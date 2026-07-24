# API Documentation

## Prediction API

### Endpoint

```
POST /predict
```

### Input

Image or webcam frame.

### Output

```json
{
  "predicted_label": "A",
  "confidence": 0.97,
  "model_version": "RandomForest_v1",
  "inference_time_ms": 23.4,
  "success": true,
  "message": "Prediction Successful"
}
```

### Error Responses

No hand detected.

Multiple hands detected.

Invalid landmark data.

Unknown gesture.