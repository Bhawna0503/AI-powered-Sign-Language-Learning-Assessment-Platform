# AI-Powered Sign Language Learning Assessment Platform

## Overview

This project is an AI-powered Sign Language Learning Assessment Platform that recognizes American Sign Language (ASL) gestures using computer vision and machine learning. The system detects hand landmarks using MediaPipe, preprocesses the landmarks, and predicts gestures using a Random Forest classifier.

---

## Features

- Static gesture recognition
- Real-time webcam recognition
- Hand landmark extraction
- Feature normalization
- Random Forest gesture classification
- Confidence score
- Model evaluation
- Benchmarking
- Future-ready sequence architecture

---

## Technologies Used

- Python
- OpenCV
- MediaPipe
- NumPy
- Pandas
- Scikit-learn
- Joblib

---

## Project Structure

```
backend/
│
├── app/
│   ├── ai/
│   ├── api/
│   ├── services/
│   └── content/
│
├── captures/
├── models/
├── output/
├── reports/
└── docs/
```

---

## Workflow

```
Image/Webcam
      │
      ▼
MediaPipe
      │
      ▼
Landmark Extraction
      │
      ▼
Normalization
      │
      ▼
Feature Vector
      │
      ▼
Random Forest
      │
      ▼
Prediction
```

---

## Future Improvements

- LSTM-based recognition
- GRU-based recognition
- Transformer-based recognition
- Sentence recognition
- Continuous sign language recognition

---

## Author

Bhavana Kasimalla