# Future Live Recognition Pipeline

## Objective

The current system recognizes one gesture from a single frame. Future versions of the project will recognize continuous sign language by analyzing sequences of frames over time.

---

## Proposed Architecture

```
Webcam Stream
      │
      ▼
Frame Capture
      │
      ▼
MediaPipe
      │
      ▼
Landmark Extraction
      │
      ▼
Temporal Buffer
      │
      ▼
Sequence Generator
      │
      ▼
Sequence Model (Future: LSTM / GRU / Transformer)
      │
      ▼
Gesture / Word Prediction
      │
      ▼
Sentence Formation
```

---

## Component Details

### 1. Webcam Stream

**Responsibility**

Captures live video from the user's webcam.

**Input**

Real-time video.

**Output**

Continuous stream of image frames.

**Why Needed**

Provides live input for gesture recognition.

---

### 2. Frame Capture

**Responsibility**

Extracts individual frames from the video stream.

**Input**

Video stream.

**Output**

Single image frame.

**Why Needed**

MediaPipe processes one frame at a time.

---

### 3. MediaPipe

**Responsibility**

Detects the user's hand and identifies hand landmarks.

**Input**

Image frame.

**Output**

21 hand landmarks.

**Why Needed**

Converts images into structured landmark data.

---

### 4. Landmark Extraction

**Responsibility**

Extracts the x, y, and z coordinates of all 21 landmarks.

**Input**

MediaPipe detection results.

**Output**

63-dimensional landmark vector.

**Why Needed**

Machine learning models require numerical features.

---

### 5. Temporal Buffer

**Responsibility**

Stores the most recent N frames.

**Input**

Current frame landmarks.

**Output**

Buffer containing the latest sequence of landmark vectors.

**Why Needed**

Dynamic gestures depend on movement over time rather than a single frame.

---

### 6. Sequence Generator

**Responsibility**

Converts buffered landmark vectors into a sequence suitable for temporal deep learning models.

**Input**

Temporal buffer.

**Output**

Sequence tensor.

**Why Needed**

LSTM, GRU, and Transformer models require sequential input.

---

### 7. Sequence Model (Future)

**Responsibility**

Learns motion patterns across multiple frames.

**Possible Models**

- LSTM
- GRU
- Transformer

**Input**

Sequence tensor.

**Output**

Gesture or word prediction.

**Why Needed**

Recognizes dynamic gestures and continuous sign language.

---

### 8. Gesture / Word Prediction

**Responsibility**

Predicts the gesture or complete signed word.

**Input**

Output from the sequence model.

**Output**

Predicted gesture label.

**Why Needed**

Transforms learned motion patterns into meaningful predictions.

---

### 9. Sentence Formation

**Responsibility**

Combines consecutive recognized gestures into meaningful sentences.

**Input**

Predicted gestures.

**Output**

Readable sentence.

**Why Needed**

Enables real-time sign language translation instead of isolated gesture recognition.

---

## Future Enhancements

- LSTM-based temporal modeling.
- Transformer-based gesture recognition.
- Multi-hand tracking.
- Face landmark integration.
- Continuous sentence translation.
- Real-time confidence visualization.
- Cloud-based inference support.