# Project Architecture

## Overview

The project is an AI-powered Sign Language Learning Assessment Platform that recognizes American Sign Language (ASL) gestures using computer vision and machine learning.

---

## Architecture

```
User
 │
 ▼
Webcam / Image
 │
 ▼
MediaPipe
 │
 ▼
Hand Detection
 │
 ▼
Landmark Extraction
 │
 ▼
Feature Preprocessing
 │
 ▼
Random Forest Model
 │
 ▼
Prediction
 │
 ▼
Backend Response
```

---

## Project Modules

### Hand Tracking

- Detects hands
- Extracts landmarks

### Feature Processing

- Landmark validation
- Wrist normalization
- Feature vector generation

### Gesture Recognition

- Model training
- Prediction

### Live Recognition

- Webcam processing
- Frame buffering
- Sequence preparation

### Evaluation

- Model evaluation
- Benchmarking