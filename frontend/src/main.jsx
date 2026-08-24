import React, { useEffect, useMemo, useRef, useState } from "react";
import { FilesetResolver, HandLandmarker } from "@mediapipe/tasks-vision";
import { createRoot } from "react-dom/client";
import "./styles.css";

const API = "/api";

const ROLE_LABELS = {
  learner: "Learner",
  instructor: "Instructor",
  trainer: "Accessibility Trainer",
  admin: "Administrator",
};

const DEMO_USERS = {
  "learner@signly.demo": { password: "learner123", role: "learner", name: "Aarav Learner" },
  "instructor@signly.demo": { password: "instructor123", role: "instructor", name: "Maya Instructor" },
  "trainer@signly.demo": { password: "trainer123", role: "trainer", name: "Riya Trainer" },
  "admin@signly.demo": { password: "admin123", role: "admin", name: "Admin User" },
};

const fallbackLessons = [
  { id: "A", title: "Letter A", level: "Beginner", category: "Alphabet", description: "Practice the static hand shape for A.", completed: true },
  { id: "B", title: "Letter B", level: "Beginner", category: "Alphabet", description: "Practice the open palm and finger alignment for B.", completed: true },
  { id: "C", title: "Letter C", level: "Beginner", category: "Alphabet", description: "Shape the curved hand position for C.", completed: false },
  { id: "D", title: "Letter D", level: "Beginner", category: "Alphabet", description: "Practice the index-finger-up configuration for D.", completed: false },
  { id: "E", title: "Letter E", level: "Beginner", category: "Alphabet", description: "Practice the closed-finger shape for E.", completed: false },
  { id: "F", title: "Letter F", level: "Beginner", category: "Alphabet", description: "Practice the thumb-index circle and raised fingers.", completed: false },
  { id: "G", title: "Letter G", level: "Beginner", category: "Alphabet", description: "Practice orientation and finger extension.", completed: false },
  { id: "H", title: "Letter H", level: "Beginner", category: "Alphabet", description: "Practice the two-finger horizontal configuration.", completed: false },
];

const seedHistory = [
  { id: 1, sign: "A", expected: "A", confidence: 0.94, accuracy: 0.94, correct: true, date: "Today", feedback: "Excellent hand shape." },
  { id: 2, sign: "B", expected: "B", confidence: 0.91, accuracy: 0.91, correct: true, date: "Yesterday", feedback: "Good finger alignment." },
  { id: 3, sign: "C", expected: "C", confidence: 0.73, accuracy: 0.70, correct: true, date: "2 days ago", feedback: "Keep the wrist steadier." },
  { id: 4, sign: "D", expected: "D", confidence: 0.51, accuracy: 0.46, correct: false, date: "3 days ago", feedback: "Raise the index finger more clearly." },
];

function readSession() {
  try { return JSON.parse(sessionStorage.getItem("signly_session") || "null"); } catch { return null; }
}
function saveSession(value) {
  if (value) sessionStorage.setItem("signly_session", JSON.stringify(value));
  else sessionStorage.removeItem("signly_session");
}
function toUnit(value) {
  const n = Number(value);
  if (!Number.isFinite(n)) return 0;
  if (n > 1) return Math.max(0, Math.min(1, n / 100));
  return Math.max(0, Math.min(1, n));
}

function pct(v) {
  return `${Math.round(toUnit(v) * 100)}%`;
}

function clamp01(v) {
  return toUnit(v);
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function apiFetch(path, options = {}) {
  const token = readSession()?.token;
  const headers = new Headers(options.headers || {});
  if (!(options.body instanceof FormData) && !headers.has("Content-Type")) headers.set("Content-Type", "application/json");
  if (token) headers.set("Authorization", `Bearer ${token}`);
  const res = await fetch(`${API}${path}`, { ...options, headers });
  if (!res.ok) {
    let detail = `Request failed (${res.status})`;
    try {
      const body = await res.json();
      detail = body.detail || body.message || detail;
    } catch {}
    const err = new Error(detail);
    err.status = res.status;
    throw err;
  }
  const type = res.headers.get("content-type") || "";
  return type.includes("application/json") ? res.json() : res.text();
}

function normalizeLessons(data) {
  const raw = Array.isArray(data) ? data : (data?.lessons || data?.items || data?.data || []);
  return raw.map((x, i) => ({
    id: String(x.id ?? x.lesson_id ?? x.letter ?? String.fromCharCode(65 + i)),
    title: x.title || x.name || `Letter ${x.letter || String.fromCharCode(65 + i)}`,
    level: x.level || x.difficulty || "Beginner",
    category: x.category || "Alphabet",
    description: x.description || x.meaning || "Practice this sign with the AI assessment engine.",
    completed: Boolean(x.completed),
  }));
}

function getLessonLetter(lesson) {
  if (!lesson) return "";

  const direct =
    lesson.letter ||
    lesson.sign ||
    lesson.gesture ||
    lesson.label;

  if (
    typeof direct === "string" &&
    /^[A-Za-z]$/.test(direct.trim())
  ) {
    return direct.trim().toUpperCase();
  }

  const title = String(lesson.title || "");
  const match = title.match(
    /(?:letter|sign|gesture)\s*[:\-]?\s*([A-Za-z])/i
  );

  return match ? match[1].toUpperCase() : "";
}

function normalizeLetter(value) {
  const s = String(value ?? "").trim().toUpperCase();
  return s;
}

function normalizePrediction(data, expected) {
  const p = data?.prediction || data?.result || data?.data || data || {};

  const detected =
    p.detected ||
    p.predicted_label ||
    p.label ||
    p.prediction ||
    p.gesture ||
    "—";

  const confidence = clamp01(
    p.confidence ?? p.score ?? p.probability ?? 0
  );

  const correct =
    p.correct != null
      ? Boolean(p.correct)
      : String(detected).trim().toUpperCase() ===
        String(expected).trim().toUpperCase();

  // Attempt accuracy is intentionally binary:
  // correct sign = 100%, incorrect sign = 0%.
  // The backend's separate "accuracy" field is not used here.
  const attemptAccuracy = correct ? 1 : 0;

  return {
    expected: String(expected),
    detected: String(detected),
    confidence,
    accuracy: attemptAccuracy,
    correct,
    inference:
      Number(
        p.inference_time ?? p.processing_time ?? p.latency ?? 0
      ) || 0,
    feedback:
      typeof p.feedback === "string"
        ? p.feedback
        : p.message ||
          (correct
            ? "Great match. Keep the same hand shape and position."
            : "Review the target hand shape and try again."),
    raw: data,
  };
}


function App() {
  const [session, setSession] = useState(readSession());
  const [route, setRoute] = useState(session ? "dashboard" : "login");
  const [lessons, setLessons] = useState(fallbackLessons);
  const [history, setHistory] = useState(seedHistory);
  const [selectedLesson, setSelectedLesson] = useState("A");
  const [notifications, setNotifications] = useState([
    { id: 1, title: "Practice reminder", text: "Review Letter D today.", unread: true },
    { id: 2, title: "Achievement", text: "You reached 3 consecutive correct signs.", unread: true },
  ]);
  const [health, setHealth] = useState("checking");

  useEffect(() => {
    fetch(`${API}/lessons/`).then(r => r.ok ? setHealth("online") : setHealth("offline")).catch(() => setHealth("offline"));
    apiFetch("/lessons/").then(data => {
      const list = normalizeLessons(data);
      if (list.length) setLessons(list);
    }).catch(() => {});
    if (session?.token) apiFetch("/auth/me").catch(() => {});
  }, [session?.token]);

  const navigate = (next) => {
    if (!session && next !== "login" && next !== "register") { setRoute("login"); return; }
    setRoute(next);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const login = async ({ email, password, role }) => {
    try {
      let result;
      const form = new URLSearchParams();
      form.set("username", email);
      form.set("password", password);
      try {
        const res = await fetch(`${API}/auth/login`, { method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" }, body: form });
        if (!res.ok) throw new Error("form");
        result = await res.json();
      } catch {
        result = await apiFetch("/auth/login", { method: "POST", body: JSON.stringify({ email, username: email, password }) });
      }
      const token = result.access_token || result.token || result.jwt;
      const user = result.user || result.profile || { email, role: result.role || role || "learner", name: result.name || email.split("@")[0] };
      const finalSession = { token, email: user.email || email, role: user.role || role || "learner", name: user.name || user.full_name || email.split("@")[0] };
      saveSession(finalSession); setSession(finalSession); setRoute("dashboard");
      return true;
    } catch (e) {
      const demo = DEMO_USERS[email.toLowerCase()];
      if (demo && demo.password === password) {
        const finalSession = { token: `demo-${Date.now()}`, email, role: demo.role, name: demo.name, demo: true };
        saveSession(finalSession); setSession(finalSession); setRoute("dashboard"); return true;
      }
      throw e;
    }
  };

  const register = async (payload) => {
    try {
      await apiFetch("/auth/register", { method: "POST", body: JSON.stringify(payload) });
      await login({ email: payload.email, password: payload.password, role: "learner" });
    } catch (e) {
      const finalSession = { token: `demo-${Date.now()}`, email: payload.email, role: "learner", name: payload.name || "New Learner", demo: true };
      saveSession(finalSession); setSession(finalSession); setRoute("dashboard");
    }
  };

  const logout = () => { saveSession(null); setSession(null); setRoute("login"); };

  if (!session && route === "register") return <AuthPage mode="register" onLogin={login} onRegister={register} goLogin={() => setRoute("login")} />;
  if (!session) return <AuthPage mode="login" onLogin={login} onRegister={register} goRegister={() => setRoute("register")} />;

  return (
    <Shell session={session} route={route} navigate={navigate} health={health} notifications={notifications} logout={logout}>
      {route === "dashboard" && <Dashboard session={session} history={history} lessons={lessons} navigate={navigate} />}
      {route === "learn" && <Learn lessons={lessons} selected={selectedLesson} setSelected={setSelectedLesson} navigate={navigate} />}
      {route === "practice" && <Practice lessons={lessons} selected={selectedLesson} setSelected={setSelectedLesson} onResult={(r) => setHistory(h => [{...r, id: Date.now(), date: "Just now", sign: r.detected}, ...h])} />}
      {route === "assessment" && <Assessment lessons={lessons} selected={selectedLesson} setSelected={setSelectedLesson} onResult={(r) => setHistory(h => [{...r, id: Date.now(), date: "Just now", sign: r.detected}, ...h])} />}
      {route === "progress" && <Progress history={history} lessons={lessons} />}
      {route === "review" && <Review history={history} navigate={navigate} />}
      {route === "certification" && <Certification history={history} />}
      {route === "reports" && <Reports history={history} session={session} />}
      {route === "notifications" && <Notifications items={notifications} setItems={setNotifications} />}
      {route === "profile" && <Profile session={session} />}
      {route === "instructor" && <Instructor history={history} />}
      {route === "trainer" && <Trainer history={history} />}
      {route === "admin" && <Admin lessons={lessons} />}
      {route === "settings" && <Settings />}
    </Shell>
  );
}

function AuthPage({ mode, onLogin, onRegister, goRegister, goLogin }) {
  const [email, setEmail] = useState(mode === "login" ? "learner@signly.demo" : "");
  const [password, setPassword] = useState(mode === "login" ? "learner123" : "");
  const [name, setName] = useState("");
  const [role, setRole] = useState("learner");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function submit(e) {
    e.preventDefault(); setError(""); setLoading(true);
    try {
      if (mode === "login") await onLogin({ email, password, role });
      else await onRegister({ email, password, name, role: "learner" });
    } catch (e) { setError(e.message || "Unable to authenticate."); }
    finally { setLoading(false); }
  }

  return (
    <div className="auth-page">
      <div className="auth-art">
        <div className="brand large"><span className="brand-mark">S</span><div><strong>Signly</strong><small>AI learning studio</small></div></div>
        <div className="auth-copy">
          <span className="eyebrow">AI-POWERED ACCESSIBILITY</span>
          <h1>Learn signs.<br/><em>Build confidence.</em></h1>
          <p>Interactive lessons, live gesture recognition, personalized feedback and measurable skill progression.</p>
          <div className="auth-proof">
            <span>✓ JWT / OAuth2</span><span>✓ AI Assessment</span><span>✓ Learning Analytics</span>
          </div>
        </div>
      </div>
      <div className="auth-card-wrap">
        <form className="auth-card" onSubmit={submit}>
          <div className="mobile-brand brand"><span className="brand-mark">S</span><div><strong>Signly</strong><small>AI learning studio</small></div></div>
          <span className="eyebrow">{mode === "login" ? "SECURE ACCESS" : "JOIN SIGNLY"}</span>
          <h2>{mode === "login" ? "Welcome back" : "Create your account"}</h2>
          <p className="muted">{mode === "login" ? "Sign in to continue your learning journey." : "Start your personalized sign-language learning path."}</p>
          {mode === "register" && <Field label="Full name"><input value={name} onChange={e=>setName(e.target.value)} placeholder="Your name" required /></Field>}
          <Field label="Email"><input type="email" value={email} onChange={e=>setEmail(e.target.value)} placeholder="you@example.com" required /></Field>
          <Field label="Password"><input type="password" value={password} onChange={e=>setPassword(e.target.value)} placeholder="••••••••" required /></Field>
          {mode === "login" && <Field label="Role"><select value={role} onChange={e=>setRole(e.target.value)}><option value="learner">Learner</option><option value="instructor">Instructor</option><option value="trainer">Accessibility Trainer</option><option value="admin">Administrator</option></select></Field>}
          {error && <div className="alert danger">{error}</div>}
          <button className="btn primary full" disabled={loading}>{loading ? "Authenticating…" : mode === "login" ? "Sign in securely" : "Create learner account"}</button>
          <div className="auth-divider"><span>OAuth2 / JWT protected</span></div>
          {mode === "login" ? <button type="button" className="link-btn" onClick={goRegister}>New to Signly? Create an account</button> : <button type="button" className="link-btn" onClick={goLogin}>Already have an account? Sign in</button>}
          <div className="demo-box"><strong>Demo accounts</strong><small>Learner: learner@signly.demo / learner123</small><small>Instructor: instructor@signly.demo / instructor123</small><small>Trainer: trainer@signly.demo / trainer123</small><small>Admin: admin@signly.demo / admin123</small></div>
        </form>
      </div>
    </div>
  );
}

function Field({ label, children }) { return <label className="field"><span>{label}</span>{children}</label>; }

function Shell({ session, route, navigate, health, notifications, logout, children }) {
  const base = [
    ["dashboard","⌂","Overview"],
    ["learn","◇","Learn"],
    ["practice","✦","Practice"],
    ["assessment","◎","Assessment"],
    ["progress","▥","Progress"],
    ["review","✓","Review"],
    ["certification","◇","Certification"],
    ["reports","▤","Reports"],
  ];
  const roleExtra = session.role === "instructor" ? [["instructor","◫","Instructor"]] :
                    session.role === "trainer" ? [["trainer","◫","Trainer"]] :
                    session.role === "admin" ? [["admin","⚙","Administration"]] : [];
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand"><span className="brand-mark">S</span><div><strong>Signly</strong><small>AI learning studio</small></div></div>
        <div className="nav-label">Workspace</div>
        <nav>{[...base, ...roleExtra].map(([r, icon, label]) => <button key={r} className={route===r?"active":""} onClick={()=>navigate(r)}><span>{icon}</span>{label}</button>)}</nav>
        <div className="sidebar-bottom">
          <button onClick={()=>navigate("notifications")}><span>◌</span>Notifications {notifications.filter(n=>n.unread).length>0 && <b className="count">{notifications.filter(n=>n.unread).length}</b>}</button>
          <button onClick={()=>navigate("profile")}><span>◎</span>Profile</button>
          <button onClick={()=>navigate("settings")}><span>⚙</span>Settings</button>
          <div className="backend-status"><i className={health==="online"?"on":health==="offline"?"off":""}></i><div><strong>{health==="online"?"AI backend online":health==="offline"?"Backend offline":"Checking backend…"}</strong><small>FastAPI connection</small></div></div>
        </div>
      </aside>
      <main className="main">
        <header className="topbar">
          <div className="crumb"><span>Workspace</span><b>/</b><strong>{routeLabel(route)}</strong></div>
          <div className="top-actions"><button className="streak">✦ 5 day streak</button><button className="avatar" onClick={()=>navigate("profile")}>{(session.name||"L").slice(0,2).toUpperCase()}</button><button className="logout" onClick={logout}>Log out</button></div>
        </header>
        <div className="content">{children}</div>
      </main>
    </div>
  );
}
function routeLabel(r) { return ({dashboard:"Overview",learn:"Learn",practice:"Practice",assessment:"Assessment",progress:"Progress",review:"Review",certification:"Certification",reports:"Reports",notifications:"Notifications",profile:"Profile",settings:"Settings",instructor:"Instructor Dashboard",trainer:"Trainer Dashboard",admin:"Administration"}[r] || "Workspace"); }

function PageHead({ eyebrow, title, subtitle, action }) {
  return <div className="page-head"><div><span className="eyebrow">{eyebrow}</span><h1>{title}</h1><p>{subtitle}</p></div>{action}</div>;
}

function Dashboard({ session, history, lessons, navigate }) {
  const avg = history.length ? history.reduce((s,x)=>s+x.accuracy,0)/history.length : 0;
  const correct = history.filter(x=>x.correct).length;
  return (
    <>
      <PageHead eyebrow="LEARNER DASHBOARD" title={`Good morning, ${session.name.split(" ")[0]}.`} subtitle="Your learning path adapts to the signs you practice and the mistakes you make." action={<button className="btn primary" onClick={()=>navigate("assessment")}>Start assessment →</button>} />
      <div className="hero-banner"><div><span className="eyebrow">CURRENT FOCUS</span><h2>Strengthen hand-shape accuracy</h2><p>Your recent attempts show a strong base. Letter D needs another focused practice round.</p><button className="btn light" onClick={()=>navigate("practice")}>Practice weak signs</button></div><div className="hero-ring"><strong>{Math.round(avg*100)}%</strong><span>accuracy</span></div></div>
      <div className="metric-grid">
        <Metric label="Overall accuracy" value={pct(avg)} trend="+8.4%" icon="◎" />
        <Metric label="Correct attempts" value={`${correct}/${history.length}`} trend="+3 this week" icon="✓" />
        <Metric label="Practice streak" value="5 days" trend="Personal best" icon="✦" />
        <Metric label="Skill level" value="Beginner" trend="62% mastery" icon="◇" />
      </div>
      <div className="grid-2">
        <section className="panel"><div className="panel-head"><div><span className="eyebrow">LEARNING PATH</span><h3>Continue learning</h3></div><button className="text-btn" onClick={()=>navigate("learn")}>View all</button></div>{lessons.slice(0,4).map(l=><LessonRow key={l.id} lesson={l} onClick={()=>navigate("learn")} />)}</section>
        <section className="panel"><div className="panel-head"><div><span className="eyebrow">AI INSIGHT</span><h3>What to practice next</h3></div></div><div className="insight"><div className="insight-icon">✦</div><div><strong>Review Letter D</strong><p>Your last D attempt was below your recent average. Focus on the raised index finger and wrist position.</p><button className="text-btn" onClick={()=>navigate("practice")}>Open practice →</button></div></div><div className="mini-score"><span>Recommended next lesson</span><strong>Everyday Communication · Greetings</strong><b>82% ready</b></div></section>
      </div>
      <section className="panel"><div className="panel-head"><div><span className="eyebrow">RECENT ACTIVITY</span><h3>Assessment history</h3></div><button className="text-btn" onClick={()=>navigate("review")}>Review all</button></div><HistoryTable history={history.slice(0,5)} /></section>
    </>
  );
}
function Metric({label,value,trend,icon}) { return <div className="metric-card"><span className="metric-icon">{icon}</span><small>{label}</small><strong>{value}</strong><span className="trend">{trend}</span></div>; }
function LessonRow({lesson,onClick}) { return <button className="lesson-row" onClick={onClick}><span className="letter">{lesson.id.slice(0,1).toUpperCase()}</span><span><strong>{lesson.title}</strong><small>{lesson.level} · {lesson.category}</small></span><span className={lesson.completed?"status done":"status"}>{lesson.completed?"✓ Complete":"Start →"}</span></button>; }

function Learn({ lessons, selected, setSelected, navigate }) {
  return <>
    <PageHead eyebrow="COURSE LIBRARY" title="Learn sign language" subtitle="Structured lessons from beginner alphabet signs to everyday communication." action={<div className="segmented"><button className="selected">Beginner</button><button>Intermediate</button><button>Advanced</button></div>} />
    <div className="course-grid"><CourseCard title="Beginner Sign Language" desc="Alphabet, hand shapes and essential everyday signs." progress="42%" count="12 lessons" active /><CourseCard title="Everyday Communication" desc="Greetings, introductions and practical communication." progress="18%" count="8 lessons" /><CourseCard title="Educational Vocabulary" desc="Useful vocabulary for learning environments." progress="0%" count="10 lessons" /></div>
    <section className="panel"><div className="panel-head"><div><span className="eyebrow">ALPHABET PRACTICE</span><h3>A–Z gesture lessons</h3></div><span className="muted">Select a lesson to practice or assess</span></div><div className="alphabet-grid">{lessons.map(l=><button key={l.id} className={`alphabet-card ${selected===l.id?"selected":""}`} onClick={()=>setSelected(l.id)}><span>{l.id}</span><strong>{l.title.replace("Letter ","")}</strong><small>{l.level}</small>{l.completed&&<b>✓</b>}</button>)}</div>{selected && <div className="lesson-detail"><div className="big-letter">{selected}</div><div><span className="eyebrow">SELECTED LESSON</span><h3>{lessons.find(l=>l.id===selected)?.title || `Letter ${selected}`}</h3><p>{lessons.find(l=>l.id===selected)?.description}</p><div className="button-row"><button className="btn secondary" onClick={()=>navigate("practice")}>Practice</button><button className="btn primary" onClick={()=>navigate("assessment")}>Assess sign</button></div></div></div>}</section>
  </>;
}
function CourseCard({title,desc,progress,count,active}) { return <div className={`course-card ${active?"featured":""}`}><div className="course-top"><span className="course-icon">◇</span><span>{count}</span></div><h3>{title}</h3><p>{desc}</p><div className="progress-line"><i style={{width:progress}}></i></div><div className="course-foot"><span>{progress} complete</span><span>View course →</span></div></div>; }

function Practice({ lessons, selected, setSelected, onResult }) {
  return <GestureWorkspace mode="practice" lessons={lessons} selected={selected} setSelected={setSelected} onResult={onResult} />;
}

function Assessment({ lessons, selected, setSelected, onResult }) {
  return <GestureWorkspace mode="assessment" lessons={lessons} selected={selected} setSelected={setSelected} onResult={onResult} />;
}

function GestureWorkspace({ mode, lessons, selected, setSelected, onResult }) {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const timerRef = useRef(null);
  const streamRef = useRef(null);
  const landmarkerRef = useRef(null);
  const animationRef = useRef(null);
  const lastVideoTimeRef = useRef(-1);

  const [camera, setCamera] = useState(false);
  const [tracking, setTracking] = useState(false);
  const [handCount, setHandCount] = useState(0);
  const [busy, setBusy] = useState(false);
  const [result, setResult] = useState(null);
  const [message, setMessage] = useState("Ready");
  const [continuous, setContinuous] = useState(false);
  const [modelLoading, setModelLoading] = useState(false);

  const target = lessons.find(
    lesson => String(lesson.id) === String(selected)
  );

  // Always use the actual ASL letter, not a numeric database lesson ID.
  const targetLabel =
    getLessonLetter(target) ||
    normalizeLetter(selected) ||
    "A";


  useEffect(() => {
    return () => {
      stopCamera();
    };
  }, []);

  async function createHandTracker() {
    if (landmarkerRef.current) return landmarkerRef.current;

    try {
      setModelLoading(true);
      setMessage("Loading MediaPipe hand model…");

      const vision = await FilesetResolver.forVisionTasks(
        "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@latest/wasm"
      );

      const tracker = await HandLandmarker.createFromOptions(vision, {
        baseOptions: {
          modelAssetPath: "/models/hand_landmarker.task",
          delegate: "CPU",
        },
        runningMode: "VIDEO",
        numHands: 2,
        minHandDetectionConfidence: 0.5,
        minHandPresenceConfidence: 0.5,
        minTrackingConfidence: 0.5,
      });

      landmarkerRef.current = tracker;
      setModelLoading(false);
      setMessage("Hand tracking active — position your hand in the frame");

      console.log("MediaPipe Hand Landmarker initialized.");
      return tracker;
    } catch (error) {
      setModelLoading(false);
      console.error("MediaPipe initialization error:", error);
      setMessage(
        "MediaPipe model could not load. Check public/models/hand_landmarker.task."
      );
      throw error;
    }
  }

  async function startCamera() {
    try {
      if (!navigator.mediaDevices?.getUserMedia) {
        throw new Error("Camera API is not available in this browser.");
      }

      setMessage("Requesting camera permission…");

      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          width: { ideal: 960 },
          height: { ideal: 720 },
          facingMode: "user",
        },
        audio: false,
      });

      streamRef.current = stream;

      const video = videoRef.current;
      if (!video) throw new Error("Video element was not found.");

      video.srcObject = stream;
      video.muted = true;
      video.playsInline = true;

      await new Promise((resolve) => {
        if (video.readyState >= 1) {
          resolve();
        } else {
          video.onloadedmetadata = () => resolve();
        }
      });

      await video.play();

      setCamera(true);
      setMessage("Initializing MediaPipe hand tracking…");

      await createHandTracker();

      setMessage("Hand tracking active — show your hand clearly");
      startTrackingLoop();

      if (continuous) {
        startAutoCapture();
      }
    } catch (error) {
      console.error("Camera startup error:", error);

      if (streamRef.current) {
        streamRef.current.getTracks().forEach((track) => track.stop());
        streamRef.current = null;
      }

      setCamera(false);
      setMessage(
        error?.name === "NotAllowedError"
          ? "Camera permission was denied. Allow camera access and try again."
          : error?.name === "NotFoundError"
          ? "No camera was found on this device."
          : error?.name === "NotReadableError"
          ? "The camera is already being used by another application."
          : error?.message || "Camera or hand-tracking model could not be initialized."
      );
    }
  }

  function stopCamera() {
    if (timerRef.current) {
      clearInterval(timerRef.current);
      timerRef.current = null;
    }

    if (animationRef.current) {
      cancelAnimationFrame(animationRef.current);
      animationRef.current = null;
    }

    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop());
      streamRef.current = null;
    }

    if (videoRef.current) {
      videoRef.current.pause();
      videoRef.current.srcObject = null;
    }

    if (landmarkerRef.current?.close) {
      try {
        landmarkerRef.current.close();
      } catch (e) {
        console.warn("MediaPipe close warning:", e);
      }
    }

    landmarkerRef.current = null;
    lastVideoTimeRef.current = -1;

    setCamera(false);
    setTracking(false);
    setHandCount(0);
    setContinuous(false);
  }

  function drawHandResults(resultData, width, height) {
    const canvas = canvasRef.current;
    if (!canvas) return;

    canvas.width = width;
    canvas.height = height;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    ctx.clearRect(0, 0, width, height);

    const hands = resultData?.landmarks || [];
    setHandCount(hands.length);
    setTracking(hands.length > 0);

    const connections = [
      [0, 1], [1, 2], [2, 3], [3, 4],
      [0, 5], [5, 6], [6, 7], [7, 8],
      [5, 9], [9, 10], [10, 11], [11, 12],
      [9, 13], [13, 14], [14, 15], [15, 16],
      [13, 17], [17, 18], [18, 19], [19, 20],
      [0, 17],
    ];

    hands.forEach((landmarks) => {
      ctx.lineWidth = Math.max(2, width / 420);
      ctx.strokeStyle = "#9b8cff";
      ctx.fillStyle = "#ffffff";
      ctx.shadowColor = "#8b78ff";
      ctx.shadowBlur = 8;

      connections.forEach(([a, b]) => {
        const p1 = landmarks[a];
        const p2 = landmarks[b];
        if (!p1 || !p2) return;

        ctx.beginPath();
        ctx.moveTo(p1.x * width, p1.y * height);
        ctx.lineTo(p2.x * width, p2.y * height);
        ctx.stroke();
      });

      landmarks.forEach((p, index) => {
        ctx.beginPath();
        ctx.arc(
          p.x * width,
          p.y * height,
          index === 0 ? 5 : 3.5,
          0,
          Math.PI * 2
        );
        ctx.fill();
      });

      ctx.shadowBlur = 0;
    });
  }

  function startTrackingLoop() {
    if (animationRef.current) {
      cancelAnimationFrame(animationRef.current);
    }

    const render = () => {
      const video = videoRef.current;
      const tracker = landmarkerRef.current;

      if (!video || !tracker || video.readyState < 2) {
        animationRef.current = requestAnimationFrame(render);
        return;
      }

      if (video.currentTime !== lastVideoTimeRef.current) {
        try {
          const timestamp = performance.now();
          const resultData = tracker.detectForVideo(video, timestamp);

          drawHandResults(
            resultData,
            video.videoWidth || 960,
            video.videoHeight || 720
          );

          lastVideoTimeRef.current = video.currentTime;
        } catch (error) {
          console.error("Hand tracking error:", error);
          setMessage("Hand tracking error. Check the browser console.");
        }
      }

      animationRef.current = requestAnimationFrame(render);
    };

    animationRef.current = requestAnimationFrame(render);
  }

  async function captureAndPredict() {
    if (!videoRef.current || !camera || busy) return;

    if (handCount !== 1) {
      setMessage(
        handCount === 0
          ? "No hand detected — place one hand clearly inside the frame."
          : "Please show exactly one hand. Multiple hands are not supported."
      );
      return;
    }

    setBusy(true);
    setMessage("Capturing stable gesture — frame 1/5…");

    try {
      const video = videoRef.current;
      const samples = [];

      // Five nearby frames make the prediction much more stable than
      // trusting one potentially noisy camera frame.
      for (let i = 0; i < 5; i++) {
        if (!videoRef.current || !camera) {
          throw new Error("Camera stopped during analysis.");
        }

        if (handCount !== 1) {
          throw new Error("Please keep exactly one hand visible.");
        }

        const canvas = document.createElement("canvas");
        canvas.width = video.videoWidth || 640;
        canvas.height = video.videoHeight || 480;

        const context = canvas.getContext("2d");
        if (!context) {
          throw new Error("Could not create capture canvas.");
        }

        context.drawImage(
          video,
          0,
          0,
          canvas.width,
          canvas.height
        );

        const blob = await new Promise(resolve =>
          canvas.toBlob(resolve, "image/jpeg", 0.92)
        );

        if (!blob) {
          throw new Error("Could not capture camera frame.");
        }

        const form = new FormData();
        form.append("file", blob, `gesture-${i + 1}.jpg`);
        form.append("expected_label", targetLabel);
        form.append("lesson_id", selected);

        setMessage(`Analyzing stable gesture — frame ${i + 1}/5…`);

        // /gesture/predict is the endpoint you already verified in Swagger.
        const data = await apiFetch("/gesture/predict", {
          method: "POST",
          body: form,
        });

        samples.push(normalizePrediction(data, targetLabel));

        if (i < 4) {
          await sleep(180);
        }
      }

      if (!samples.length) {
        throw new Error("No prediction was returned by the backend.");
      }

      // Weighted voting: a frame with higher model confidence contributes
      // more to its predicted label.
      const votes = new Map();

      for (const sample of samples) {
        const key = sample.detected.trim().toUpperCase();
        const weight = Math.max(sample.confidence, 0.01);

        if (!votes.has(key)) {
          votes.set(key, {
            label: sample.detected,
            weight: 0,
            count: 0,
            feedback: sample.feedback,
          });
        }

        const vote = votes.get(key);
        vote.weight += weight;
        vote.count += 1;

        if (sample.confidence >= 0.8) {
          vote.feedback = sample.feedback;
        }
      }

      const winner = [...votes.values()].sort(
        (a, b) => b.weight - a.weight || b.count - a.count
      )[0];

      const winningSamples = samples.filter(
        sample =>
          sample.detected.trim().toUpperCase() ===
          winner.label.trim().toUpperCase()
      );

      const stableConfidence =
        winningSamples.reduce(
          (sum, sample) => sum + sample.confidence,
          0
        ) / Math.max(winningSamples.length, 1);

      const frameAgreement =
        winningSamples.length / samples.length;

      const detected =
        normalizeLetter(winner.label) || winner.label;

      const labelMatches =
        detected.trim().toUpperCase() ===
        targetLabel.trim().toUpperCase();

      // Require a genuinely stable webcam result.
      // 4/5 or 5/5 frames must agree, and winning-frame confidence
      // must be at least 60%.
      const stableEnough =
        frameAgreement >= 0.80 &&
        stableConfidence >= 0.60;

      const correct =
        labelMatches && stableEnough;

      const averageInference =
        samples.reduce(
          (sum, sample) => sum + sample.inference,
          0
        ) / samples.length;

      // NEVER use winner.feedback here.
      // Backend/per-frame feedback can contain a stale expected letter.
      const agreementText =
        `${winningSamples.length}/${samples.length} frames agreed (${Math.round(
          frameAgreement * 100
        )}%).`;

      const finalFeedback = correct
        ? [
            `Correct! The expected sign is ${targetLabel} and the detected sign is ${detected}.`,
            `Stable prediction: ${agreementText}`,
            stableConfidence >= 0.80
              ? "Excellent model confidence and consistency."
              : "Good confidence. Keep your hand steady for even more consistent results.",
          ]
        : labelMatches
        ? [
            `The model detected ${detected}, but the prediction was not stable enough.`,
            `Stable prediction: ${agreementText}`,
            `Model confidence: ${Math.round(
              stableConfidence * 100
            )}%. Hold the ${targetLabel} sign steady and try again.`,
          ]
        : [
            `Expected ${targetLabel}, but the model detected ${detected}.`,
            `Stable prediction: ${agreementText}`,
            "Review the target hand shape and try again.",
          ];

      const stableResult = {
        expected: targetLabel,
        detected,
        confidence: stableConfidence,
        accuracy: correct ? 1 : 0,
        correct,
        inference: averageInference,
        frameAgreement,
        framesAnalyzed: samples.length,
        winningFrames: winningSamples.length,
        stableEnough,
        samples,
        feedback: finalFeedback,
        raw: samples.map(sample => sample.raw),
      };

      setResult(stableResult);
      onResult(stableResult);

      setMessage(
        correct
          ? "✓ Correct sign detected with stable frame agreement"
          : "Try again — keep one hand centered and review the feedback"
      );
    } catch (error) {
      console.error("Prediction error:", error);

      setMessage(
        error?.message ||
          "Prediction endpoint could not be reached. Check FastAPI and /gesture/predict."
      );
    } finally {
      setBusy(false);
    }
  }

  function startAutoCapture() {
    if (timerRef.current) {
      clearInterval(timerRef.current);
    }

    timerRef.current = setInterval(() => {
      captureAndPredict();
    }, 1800);
  }

  function toggleAutoScan() {
    setContinuous((previous) => {
      const next = !previous;

      if (next) {
        startAutoCapture();
      } else if (timerRef.current) {
        clearInterval(timerRef.current);
        timerRef.current = null;
      }

      return next;
    });
  }

  return (
    <>
      <PageHead
        eyebrow={mode === "assessment" ? "ASSESSMENT" : "PRACTICE"}
        title={`${mode === "assessment" ? "Assessment" : "Practice"} · ${
          target?.title || `Letter ${selected}`
        }`}
        subtitle={
          mode === "assessment"
            ? "Perform the expected sign and receive instant AI feedback."
            : "Use the camera to practice a target sign and build confidence."
        }
        action={
          <div className="select-wrap">
            <span>Target</span>
            <select
              value={selected}
              onChange={(e) => {
                setSelected(e.target.value);
                setResult(null);
              }}
              disabled={busy}
            >
              {lessons.map((l) => (
                <option key={l.id} value={l.id}>
                  {l.title}
                </option>
              ))}
            </select>
          </div>
        }
      />

      <div className="assessment-grid">
        <section className="camera-panel panel">
          <div className="camera-toolbar">
            <span className={camera ? "live-dot" : "ready-dot"}></span>

            <strong>
              {camera
                ? tracking
                  ? `HAND TRACKING · ${handCount} HAND${handCount === 1 ? "" : "S"}`
                  : modelLoading
                  ? "LOADING HAND TRACKER"
                  : "LIVE CAMERA · SEARCHING FOR HAND"
                : "CAMERA READY"}
            </strong>

            <span className="camera-tip">
              21-point landmarks · one hand · good lighting
            </span>
          </div>

          <div className="camera-stage">
            <video
              ref={videoRef}
              muted
              autoPlay
              playsInline
              className={camera ? "video live" : "video hidden"}
            />

            <canvas
              ref={canvasRef}
              className={camera ? "tracking-canvas" : "hidden"}
            />

            {!camera && (
              <div className="camera-placeholder">
                <div className="target-orb">
                  <span>{selected}</span>
                </div>

                <h3>Target {selected}</h3>

                <p>
                  Start the webcam to activate live MediaPipe hand tracking.
                  The hand skeleton will appear over your hand as you move.
                </p>
              </div>
            )}

            {camera && (
              <>
                <div className="camera-overlay">
                  <span>Expected: {selected}</span>

                  <span>
                    {tracking ? "● Hand detected" : "○ Show your hand"}
                  </span>
                </div>

                <div className="tracking-status">
                  <span
                    className={
                      tracking
                        ? "status-indicator active"
                        : "status-indicator"
                    }
                  ></span>

                  {tracking
                    ? `${handCount} hand${
                        handCount === 1 ? "" : "s"
                      } tracked · 21 landmarks`
                    : "Searching for a hand…"}
                </div>
              </>
            )}
          </div>

          <div className="camera-actions">
            {!camera ? (
              <button
                className="btn primary full"
                onClick={startCamera}
                disabled={modelLoading}
              >
                {modelLoading
                  ? "Loading AI model…"
                  : "◉ Start webcam + hand tracking"}
              </button>
            ) : (
              <>
                <button
                  className="btn primary"
                  disabled={busy || handCount === 0}
                  onClick={captureAndPredict}
                >
                  {busy ? "Analyzing…" : "Capture & assess"}
                </button>

                <button
                  className="btn secondary"
                  onClick={toggleAutoScan}
                >
                  {continuous ? "Stop auto scan" : "Auto scan"}
                </button>

                <button
                  className="btn ghost"
                  onClick={stopCamera}
                >
                  Stop camera
                </button>
              </>
            )}
          </div>

          <div className="tracking-info">
            <div>
              <strong>{handCount}</strong>
              <span>hands</span>
            </div>

            <div>
              <strong>{tracking ? "LIVE" : "—"}</strong>
              <span>tracking</span>
            </div>

            <div>
              <strong>{tracking ? "21" : "—"}</strong>
              <span>landmarks / hand</span>
            </div>

            <div>
              <strong>VIDEO</strong>
              <span>MediaPipe mode</span>
            </div>
          </div>

          <div className="pipeline">
            <PipelineStep ok={camera} label="Camera frame" />
            <PipelineStep ok={tracking} label="Hand tracking" />
            <PipelineStep ok={tracking} label="21 landmarks" />
            <PipelineStep ok={!!result} label="Random Forest" />
            <PipelineStep ok={!!result} label="Assessment + feedback" />
          </div>

          <div className="camera-message">{message}</div>
        </section>

        <section className="result-panel panel">
          <div className="panel-head">
            <div>
              <span className="eyebrow">LIVE RESULT</span>

              <h3>
                {result
                  ? result.correct
                    ? "Great match!"
                    : "Let's correct it"
                  : tracking
                  ? "Hand detected"
                  : "Waiting for gesture"}
              </h3>
            </div>

            <span className="badge">
              {result ? "Analyzed" : tracking ? "Tracking" : "Ready"}
            </span>
          </div>

          <div className="result-compare">
            <div>
              <small>EXPECTED</small>
              <strong>{targetLabel}</strong>
            </div>

            <div className="arrow">→</div>

            <div>
              <small>DETECTED</small>
              <strong className={result?.correct ? "good" : ""}>
                {result?.detected || "—"}
              </strong>
            </div>
          </div>

          <ScoreBar
            label="Model confidence"
            value={result?.confidence || 0}
          />

          <ScoreBar
            label="Attempt accuracy"
            value={result?.accuracy || 0}
          />

          {result?.frameAgreement != null && (
            <ScoreBar
              label="Frame agreement"
              value={result.frameAgreement}
            />
          )}

          <div className="result-meta">
            <span>Inference time</span>

            <strong>
              {result?.inference
                ? `${result.inference.toFixed(3)}s`
                : "—"}
            </strong>
          </div>

          <div className={`feedback ${result?.correct ? "success" : ""}`}>
            <span>{result?.correct ? "✓" : "✦"}</span>

            <div>
              <strong>{result ? "AI feedback" : "Feedback"}</strong>

              <p>
                {result?.feedback ||
                  "Start hand tracking and submit a frame to see prediction, confidence and rule-based feedback."}
              </p>
            </div>
          </div>

          {result && (
            <div className="save-note">
              ✓ Assessment attempt added to your learning history.
            </div>
          )}
        </section>
      </div>
    </>
  );
}

function PipelineStep({ok,label}) { return <div className={ok?"pipe ok":"pipe"}><span>{ok?"✓":"○"}</span>{label}</div>; }
function ScoreBar({label,value}) { return <div className="scorebar"><div><span>{label}</span><b>{pct(value)}</b></div><i><em style={{width:`${clamp01(value)*100}%`}}></em></i></div>; }

function Progress({history,lessons}) {
  const avg = history.length ? history.reduce((s,x)=>s+x.accuracy,0)/history.length : 0;
  const correct = history.filter(x=>x.correct).length;
  const weak = [...history].sort((a,b)=>a.accuracy-b.accuracy)[0]?.expected || "D";
  const mastery = Math.min(100, Math.round(avg*100 + lessons.filter(l=>l.completed).length*3));
  return <>
    <PageHead eyebrow="LEARNING INTELLIGENCE" title="Your progress" subtitle="Track accuracy, mastery, consistency and the areas that need attention." />
    <div className="metric-grid"><Metric label="Overall score" value={`${mastery}`} trend="/ 100" icon="✦"/><Metric label="Gesture accuracy" value={pct(avg)} trend="40% weight" icon="◎"/><Metric label="Assessment performance" value={pct(avg*.95)} trend="25% weight" icon="✓"/><Metric label="Lesson completion" value={`${lessons.filter(l=>l.completed).length}/${lessons.length}`} trend="15% weight" icon="◇"/></div>
    <div className="grid-2"><section className="panel"><div className="panel-head"><div><span className="eyebrow">SKILL MASTERY</span><h3>Alphabet performance</h3></div></div><div className="skill-list">{["A","B","C","D","E","F"].map((s,i)=>{const h=history.filter(x=>x.expected===s);const v=h.length?h.reduce((a,x)=>a+x.accuracy,0)/h.length:0.25+i*.06;return <div className="skill-row" key={s}><span className="skill-letter">{s}</span><div><strong>Letter {s}</strong><div className="progress-line"><i style={{width:`${Math.round(v*100)}%`}}></i></div></div><b>{Math.round(v*100)}%</b></div>})}</div></section><section className="panel"><div className="panel-head"><div><span className="eyebrow">WEAK AREA</span><h3>Recommended focus</h3></div></div><div className="focus-card"><div className="focus-letter">{weak}</div><div><strong>Review Letter {weak}</strong><p>Your lowest recent performance is here. A focused practice round can raise your mastery.</p><button className="btn primary">Practice now →</button></div></div><div className="weight-list"><span>Gesture accuracy <b>40%</b></span><span>Assessment performance <b>25%</b></span><span>Lesson completion <b>15%</b></span><span>Practice consistency <b>10%</b></span><span>Improvement rate <b>10%</b></span></div></section></div>
    <section className="panel"><div className="panel-head"><div><span className="eyebrow">RECENT PERFORMANCE</span><h3>Assessment history</h3></div><span className="muted">{correct} correct of {history.length}</span></div><HistoryTable history={history}/></section>
  </>;
}

function HistoryTable({history}) { return <div className="table-wrap"><table><thead><tr><th>Sign</th><th>Expected</th><th>Detected</th><th>Confidence</th><th>Accuracy</th><th>Result</th><th>Date</th></tr></thead><tbody>{history.map(h=><tr key={h.id}><td><span className="table-letter">{h.sign}</span></td><td>{h.expected}</td><td>{h.detected}</td><td>{pct(h.confidence)}</td><td>{pct(h.accuracy)}</td><td><span className={h.correct?"result-pill good":"result-pill bad"}>{h.correct?"Correct":"Review"}</span></td><td>{h.date}</td></tr>)}</tbody></table></div>; }

function Review({history,navigate}) {
  const wrong = history.filter(h=>!h.correct);
  return <>
    <PageHead eyebrow="AI REVIEW" title="Review & improve" subtitle="Turn assessment mistakes into targeted learning actions." action={<button className="btn primary" onClick={()=>navigate("practice")}>Practice weak area →</button>} />
    <div className="review-grid"><div className="review-hero"><span className="eyebrow">PERSONALIZED PLAN</span><h2>Three small improvements can unlock your next level.</h2><p>Focus on hand shape first, then stabilize wrist position. Finish with a short timed assessment.</p><div className="plan-steps"><span>01 Hand shape</span><span>02 Position</span><span>03 Timed assessment</span></div></div><section className="panel"><div className="panel-head"><div><span className="eyebrow">ERROR ANALYSIS</span><h3>What needs attention?</h3></div></div>{wrong.length ? wrong.map(h=><div className="error-card" key={h.id}><div className="error-icon">!</div><div><strong>Letter {h.expected}</strong><p>{h.feedback}</p><span>Confidence {pct(h.confidence)}</span></div><button className="text-btn">Review →</button></div>) : <div className="empty-state">No incorrect attempts yet. Keep practicing to build consistency.</div>}</section></div>
    <section className="panel"><div className="panel-head"><div><span className="eyebrow">AI GUIDANCE</span><h3>Personalized improvement plan</h3></div></div><div className="recommend-grid"><Recommendation n="01" title="Practice weak signs" text="Repeat your lowest-confidence signs until the result is stable."/><Recommendation n="02" title="Review lesson content" text="Return to the hand-shape guide before your next assessment."/><Recommendation n="03" title="Retake assessment" text="Complete a clean run with one hand centered in the camera frame."/></div></section>
  </>;
}
function Recommendation({n,title,text}) { return <div className="recommend"><span>{n}</span><div><strong>{title}</strong><p>{text}</p></div><span>→</span></div>; }

function Certification({history}) {
  const score = history.length ? Math.round(history.reduce((s,x)=>s+x.accuracy,0)/history.length*100) : 0;
  const ready = score >= 80 && history.length >= 5;
  return <>
    <PageHead eyebrow="CERTIFICATION" title="Skill certification" subtitle="Evaluate your readiness and complete a structured certification assessment." />
    <div className="cert-banner"><div><span className="eyebrow">CURRENT LEVEL</span><h2>Beginner Sign Language</h2><p>Complete the readiness checklist before starting your certification exam.</p></div><div className={`cert-score ${ready?"ready":""}`}><strong>{score}</strong><span>readiness</span></div></div>
    <div className="cert-grid"><section className="panel"><div className="panel-head"><div><span className="eyebrow">READINESS CHECK</span><h3>Before you start</h3></div></div><Check label="Gesture accuracy ≥ 80%" ok={score>=80}/><Check label="At least 5 assessment attempts" ok={history.length>=5}/><Check label="Review weak areas" ok={history.some(h=>!h.correct)}/><Check label="Consistent practice streak" ok={true}/><button className="btn primary full" disabled={!ready}>Start certification exam →</button></section><section className="panel"><div className="panel-head"><div><span className="eyebrow">CERTIFICATE</span><h3>Achievement preview</h3></div></div><div className="certificate"><div className="cert-mark">S</div><span>Certificate of Skill</span><h3>{ready?"Ready to certify":"Keep learning"}</h3><p>Signly Sign Language Learning & Assessment Platform</p><small>Your verified achievement will appear here after a successful exam.</small></div></section></div>
  </>;
}
function Check({label,ok}) { return <div className="check-row"><span className={ok?"check ok":"check"}>{ok?"✓":"○"}</span><span>{label}</span><b>{ok?"Complete":"Pending"}</b></div>; }

function Reports({history,session}) {
  const score = history.length ? history.reduce((s,x)=>s+x.accuracy,0)/history.length : 0;
  function print(){window.print();}
  function csv(){const rows=[["Sign","Expected","Detected","Confidence","Accuracy","Correct","Date"],...history.map(h=>[h.sign,h.expected,h.detected,pct(h.confidence),pct(h.accuracy),h.correct,h.date])];const blob=new Blob([rows.map(r=>r.join(",")).join("\n")],{type:"text/csv"});const a=document.createElement("a");a.href=URL.createObjectURL(blob);a.download="signly-progress-report.csv";a.click();}
  return <>
    <PageHead eyebrow="REPORTS & EXPORT" title="Learning reports" subtitle="Generate performance, assessment and progress reports for your learning journey." action={<div className="button-row"><button className="btn secondary" onClick={print}>Print / PDF</button><button className="btn primary" onClick={csv}>Export Excel-compatible CSV</button></div>} />
    <section className="report-cover"><div><span className="eyebrow">SIGNLY PERFORMANCE REPORT</span><h2>{session.name}</h2><p>Role: {ROLE_LABELS[session.role] || session.role} · Generated {new Date().toLocaleDateString()}</p></div><strong>{Math.round(score*100)}<small>/100</small></strong></section>
    <div className="metric-grid"><Metric label="Gesture accuracy" value={pct(score)} trend="40%" icon="◎"/><Metric label="Assessment performance" value={pct(score*.95)} trend="25%" icon="✓"/><Metric label="Practice consistency" value="78%" trend="10%" icon="✦"/><Metric label="Improvement rate" value="+12%" trend="10%" icon="↗"/></div>
    <section className="panel"><div className="panel-head"><div><span className="eyebrow">ASSESSMENT REPORT</span><h3>Detailed attempts</h3></div></div><HistoryTable history={history}/></section>
  </>;
}

function Notifications({items,setItems}) {
  return <><PageHead eyebrow="NOTIFICATIONS" title="Stay on track" subtitle="Practice reminders, assessment alerts and achievements." action={<button className="btn secondary" onClick={()=>setItems(items.map(x=>({...x,unread:false})))}>Mark all read</button>} /><div className="notification-list">{items.map(n=><div className={`notification ${n.unread?"unread":""}`} key={n.id}><span className="notification-icon">✦</span><div><strong>{n.title}</strong><p>{n.text}</p></div><small>Today</small></div>)}</div></>;
}

function Profile({session}) { return <><PageHead eyebrow="LEARNER PROFILE" title="Your profile" subtitle="Manage learning preferences, goals and account information."/><div className="profile-grid"><section className="panel profile-card"><div className="profile-avatar">{session.name.slice(0,2).toUpperCase()}</div><h2>{session.name}</h2><p>{session.email}</p><span className="role-chip">{ROLE_LABELS[session.role]}</span><div className="profile-fields"><Field label="Learning level"><select defaultValue="Beginner"><option>Beginner</option><option>Intermediate</option><option>Advanced</option></select></Field><Field label="Preferred language"><select defaultValue="English"><option>English</option><option>Telugu</option><option>Hindi</option></select></Field></div></section><section className="panel"><div className="panel-head"><div><span className="eyebrow">LEARNING GOALS</span><h3>What are you working toward?</h3></div></div><div className="goal-grid"><Goal title="Everyday communication" active/><Goal title="Educational vocabulary"/><Goal title="Professional communication"/><Goal title="Accessibility confidence"/></div><div className="panel-divider"></div><span className="eyebrow">ACCOUNT SECURITY</span><p className="muted">Authentication is handled by the FastAPI JWT/OAuth2 backend. Your API requests use a bearer access token.</p></section></div></>; }
function Goal({title,active}) { return <button className={`goal ${active?"active":""}`}><span>{active?"✓":"○"}</span>{title}</button>; }

function Instructor({history}) { return <><PageHead eyebrow="INSTRUCTOR PORTAL" title="Learner performance" subtitle="Monitor student progress, assessment reports and class-level trends."/><div className="metric-grid"><Metric label="Active learners" value="24" trend="+4 this week" icon="◎"/><Metric label="Avg. accuracy" value="86%" trend="+6.2%" icon="✓"/><Metric label="Assessments" value="148" trend="This month" icon="▥"/><Metric label="At-risk learners" value="3" trend="Needs review" icon="!"/></div><div className="grid-2"><section className="panel"><div className="panel-head"><div><span className="eyebrow">CLASS PROGRESS</span><h3>Learning analytics</h3></div></div>{["Aarav · Beginner","Meera · Beginner","Sahil · Intermediate","Ananya · Beginner"].map((x,i)=><div className="student-row" key={x}><span className="student-avatar">{x[0]}</span><div><strong>{x}</strong><small>{i===2?"Advanced lesson":"Alphabet course"}</small></div><b>{92-i*7}%</b></div>)}</section><section className="panel"><div className="panel-head"><div><span className="eyebrow">ASSESSMENT REPORTS</span><h3>Recent activity</h3></div></div><HistoryTable history={history.slice(0,4)}/></section></div></>; }

function Trainer({history}) { return <><PageHead eyebrow="ACCESSIBILITY TRAINER" title="Learner support" subtitle="Monitor engagement, skill development and certification readiness."/><div className="metric-grid"><Metric label="Learner engagement" value="91%" trend="+4.1%" icon="◎"/><Metric label="Skill development" value="84%" trend="+8.3%" icon="↗"/><Metric label="Assessment readiness" value="76%" trend="12 learners" icon="✓"/><Metric label="Certification watch" value="5" trend="This week" icon="◇"/></div><section className="panel"><div className="panel-head"><div><span className="eyebrow">SUPPORT QUEUE</span><h3>Recommended interventions</h3></div></div><div className="recommend-grid"><Recommendation n="01" title="Review hand-shape errors" text="Three learners have repeated the same hand-shape mistake more than twice."/><Recommendation n="02" title="Schedule assessment review" text="Five learners are approaching certification readiness."/><Recommendation n="03" title="Engagement reminder" text="Send a practice reminder to learners inactive for three days."/></div></section></>; }

function Admin({lessons}) { return <><PageHead eyebrow="ADMINISTRATION" title="Platform control center" subtitle="Manage users, content, platform analytics and system health."/><div className="metric-grid"><Metric label="Registered users" value="312" trend="+18 this month" icon="◎"/><Metric label="Lessons" value={lessons.length} trend="Alphabet loaded" icon="◇"/><Metric label="API uptime" value="99.8%" trend="Healthy" icon="✓"/><Metric label="AI inferences" value="12.8K" trend="This month" icon="✦"/></div><div className="admin-grid"><AdminCard title="User management" items={["Learners · 274","Instructors · 18","Trainers · 14","Administrators · 6"]}/><AdminCard title="Content management" items={["Beginner Sign Language","Intermediate Sign Language","Advanced Sign Language","Everyday Communication"]}/><AdminCard title="System monitoring" items={["FastAPI · Online","AI model · Ready","Database · Connected","Logging · Active"]}/></div></>; }
function AdminCard({title,items}) { return <section className="panel"><div className="panel-head"><h3>{title}</h3><button className="text-btn">Manage →</button></div>{items.map(x=><div className="admin-item" key={x}><span>◇</span>{x}<b>›</b></div>)}</section>; }

function Settings() { return <><PageHead eyebrow="SETTINGS" title="Workspace settings" subtitle="Configure your learning experience and system preferences."/><section className="panel settings-list"><Setting title="Auto-scan during assessment" desc="Continuously capture frames while the webcam is active." on/><Setting title="Instant AI feedback" desc="Show feedback immediately after each prediction." on/><Setting title="Practice reminders" desc="Receive reminders when your learning streak is at risk." on/><Setting title="Reduced motion" desc="Use simpler transitions for accessibility." /></section></>; }
function Setting({title,desc,on}) { const [v,setV]=useState(on); return <div className="setting"><div><strong>{title}</strong><p>{desc}</p></div><button className={`toggle ${v?"on":""}`} onClick={()=>setV(!v)}><i></i></button></div>; }

createRoot(document.getElementById("root")).render(<App />);