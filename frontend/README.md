# Signly — Final Frontend

React + Vite frontend designed from the supplied Sign Language Learning & Assessment Platform requirements.

## Included flows

- JWT/OAuth2-style login/register flow against FastAPI
- Learner, Instructor, Accessibility Trainer, and Administrator workspaces
- Learner profile and goals
- Course/lesson browsing
- Webcam practice
- Live assessment capture
- `/assessment/predict` integration
- Expected vs detected sign
- Confidence, accuracy and inference time
- Feedback and error-analysis presentation
- Progress and mastery dashboard
- Personalized recommendations
- Performance scoring using the PDF's 40/25/15/10/10 weighting
- Instructor analytics
- Accessibility Trainer analytics
- Admin content/system/user views
- Certification readiness and exam flow
- Reports with print/export
- Notifications/reminders UI
- Responsive mobile/tablet/desktop layout
- API health indicator
- Graceful fallback when an optional endpoint is unavailable

## Run

1. Keep FastAPI running at `http://127.0.0.1:8000`.
2. From this frontend directory:

```powershell
npm install
npm run dev
```

3. Open `http://localhost:5173`.

## API integration

The Vite proxy maps `/api/*` to `http://127.0.0.1:8000/*`.

Expected core endpoints:
- `POST /auth/login`
- `POST /auth/register`
- `GET /auth/me`
- `GET /lessons/`
- `GET /lessons/{lesson_id}`
- `POST /assessment/start/{lesson_id}`
- `POST /assessment/predict`
- `POST /assessment/end`
- session/gesture endpoints as available

The client normalizes common response shapes so the UI remains usable while the backend is being completed.


## Live hand tracking

The webcam assessment now uses MediaPipe Hand Landmarker in the browser. When the webcam starts:
- MediaPipe runs in VIDEO mode.
- Up to 2 hands can be tracked.
- 21 landmarks per hand are drawn as a live skeleton overlay.
- The UI shows hand count and tracking status.
- Capture is disabled until a hand is detected.
- The captured frame is still sent to the FastAPI assessment endpoint for your project's Random Forest prediction/feedback pipeline.

The MediaPipe web package is installed through `@mediapipe/tasks-vision`.
