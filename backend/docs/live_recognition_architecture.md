# Live Recognition Architecture

## Overview

The Sign Language Learning Assessment Platform currently recognizes a single gesture from an image or webcam frame using a Random Forest classifier. The architecture is designed so that it can be upgraded in the future to support continuous sign language recognition using sequence models such as LSTM, GRU, or Transformer.

---

## Current Architecture

```
Webcam
    │
    ▼
Frame Capture
    │
    ▼
MediaPipe Hand Detection
    │
    ▼
Landmark Extraction
    │
    ▼
Landmark Validation
    │
    ▼
Feature Normalization
    │
    ▼
Feature Vector Generation
    │
    ▼
Random Forest Model
    │
    ▼
Gesture Prediction
```

---

## Future Architecture

```
Webcam
    │
    ▼
Frame Capture
    │
    ▼
MediaPipe Hand Detection
    │
    ▼
Landmark Extraction
    │
    ▼
Frame Buffer
    │
    ▼
Sequence Builder
    │
    ▼
LSTM / GRU / Transformer
    │
    ▼
Gesture Prediction
```

---

## Component Description

### Webcam

Purpose:
Capture live video frames.

Input:
Live video.

Output:
Video frames.

Why Required:
Provides real-time gesture input.

---

### Frame Capture

Purpose:
Reads frames continuously.

Input:
Webcam stream.

Output:
Individual image frames.

Why Required:
Supplies frames for processing.

---

### MediaPipe Hand Detection

Purpose:
Detects hands in the frame.

Input:
Image frame.

Output:
Hand landmarks.

Why Required:
Locates the hand accurately.

---

### Landmark Extraction

Purpose:
Extracts 21 hand landmarks.

Input:
Detected hand.

Output:
21 landmark coordinates.

Why Required:
Creates gesture features.

---

### Frame Buffer

Purpose:
Stores the latest 20–30 frames.

Input:
Landmark vectors.

Output:
Buffered sequence.

Why Required:
Prepares data for temporal models.

---

### Sequence Builder

Purpose:
Creates a sequence tensor.

Input:
Buffered landmark vectors.

Output:
20 × 63 feature tensor.

Why Required:
Required for LSTM/GRU/Transformer.

---

### Random Forest

Purpose:
Current gesture classifier.

Input:
63-dimensional feature vector.

Output:
Predicted gesture.

Why Required:
Fast and accurate for static gestures.

---

### LSTM / GRU / Transformer

Purpose:
Future sequence recognition.

Input:
Sequence tensor.

Output:
Continuous gesture prediction.

Why Required:
Captures temporal motion between frames.