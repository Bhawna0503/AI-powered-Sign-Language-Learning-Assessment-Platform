# Installation Guide

## Clone Repository

```bash
git clone <repository_url>
```

## Create Virtual Environment

```bash
python -m venv venv
```

## Activate Environment

Windows

```bash
venv\Scripts\activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Train Model

```bash
python app/ai/gesture_recognition/train_model.py
```

## Evaluate Model

```bash
python app/ai/evaluation/evaluate_model.py
```

## Run Image Prediction

```bash
python test_prediction.py
```

## Run Live Recognition

```bash
python -m app.ai.live_recognition.live_pipeline
```