# API Documentation

Complete API reference for the X-Ray Medical Image Classification system.

## Base URL

Development: `http://localhost:5000`
Production: `https://your-deployed-app.com`

## Authentication

Currently, no authentication is required. For production, consider implementing:
- API key authentication
- JWT tokens
- OAuth2

## Endpoints

### 1. Home Page
Get the web interface.

```http
GET /
```

**Response:** HTML page with upload form

**Example:**
```bash
curl http://localhost:5000/
```

---

### 2. Upload and Predict (Web)
Submit X-Ray image for classification via web form.

```http
POST /
```

**Parameters:**
- `file` (form-data, required): Image file (JPG, PNG, GIF, BMP, DICOM)

**Response:** HTML result page with classification

**Example:**
```bash
curl -X POST -F "file=@xray.jpg" http://localhost:5000/
```

---

### 3. API Prediction
Get classification result as JSON.

```http
POST /api/predict
```

**Parameters:**
- `file` (form-data, required): Image file

**Response:**
```json
{
  "success": true,
  "class": "Normal",
  "confidence": 95.23,
  "confidence_score": 0.9523,
  "top_3_predictions": [
    {
      "class": "Normal",
      "confidence": 95.23
    },
    {
      "class": "Hairline Fracture",
      "confidence": 3.45
    },
    {
      "class": "Transverse Fracture",
      "confidence": 1.32
    }
  ],
  "probabilities": {
    "Avulsion Fracture": 0.12,
    "Comminuted Fracture": 0.08,
    "Fracture Dislocation": 0.15,
    "Greenstick Fracture": 0.05,
    "Hairline Fracture": 3.45,
    "Impacted Fracture": 0.09,
    "Longitudinal Fracture": 0.11,
    "Normal": 95.23,
    "Oblique Fracture": 0.18,
    "Pathological Fracture": 0.06,
    "Spiral Fracture": 0.13,
    "Transverse Fracture": 1.32
  }
}
```

**Status Codes:**
- `200`: Success
- `400`: Bad request (invalid file)
- `413`: File too large
- `500`: Server error

**Example:**
```bash
curl -X POST \
  -F "file=@xray.jpg" \
  http://localhost:5000/api/predict | jq
```

**Python Example:**
```python
import requests

url = "http://localhost:5000/api/predict"
files = {"file": open("xray.jpg", "rb")}

response = requests.post(url, files=files)
result = response.json()

print(f"Classification: {result['class']}")
print(f"Confidence: {result['confidence']:.2f}%")
```

---

### 4. API Information
Get API metadata and supported classes.

```http
GET /api/info
```

**Response:**
```json
{
  "app_name": "X-Ray Medical Image Classification",
  "version": "1.0.0",
  "model": "DenseNet",
  "classes": [
    "Avulsion Fracture",
    "Comminuted Fracture",
    "Fracture Dislocation",
    "Greenstick Fracture",
    "Hairline Fracture",
    "Impacted Fracture",
    "Longitudinal Fracture",
    "Normal",
    "Oblique Fracture",
    "Pathological Fracture",
    "Spiral Fracture",
    "Transverse Fracture"
  ],
  "max_file_size_mb": 16.0,
  "allowed_extensions": [
    "jpg",
    "jpeg",
    "png",
    "gif",
    "bmp",
    "dicom",
    "dcm"
  ]
}
```

**Example:**
```bash
curl http://localhost:5000/api/info | jq
```

---

### 5. Health Check
Check if the application and model are running.

```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

**Status Codes:**
- `200`: Application is healthy

**Example:**
```bash
curl http://localhost:5000/health
```

**Use in Docker:**
```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1
```

---

## Error Responses

### Bad Request (400)
```json
{
  "error": "No file provided"
}
```

### File Too Large (413)
```json
{
  "error": "File too large. Maximum size: 16.0MB"
}
```

### Internal Error (500)
```json
{
  "error": "Prediction error: [detailed error message]"
}
```

---

## Usage Examples

### JavaScript (Fetch)
```javascript
async function predictImage(imageFile) {
  const formData = new FormData();
  formData.append('file', imageFile);
  
  const response = await fetch('/api/predict', {
    method: 'POST',
    body: formData
  });
  
  const result = await response.json();
  console.log(`Classification: ${result.class}`);
  console.log(`Confidence: ${result.confidence.toFixed(2)}%`);
  return result;
}

// Usage
document.getElementById('fileInput').addEventListener('change', async (e) => {
  const file = e.target.files[0];
  const result = await predictImage(file);
  displayResults(result);
});
```

### Python (Requests)
```python
import requests
import json

def predict_image(image_path):
    with open(image_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(
            'http://localhost:5000/api/predict',
            files=files
        )
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

# Get API info
info_response = requests.get('http://localhost:5000/api/info')
api_info = info_response.json()
print(f"Supported classes: {api_info['classes']}")

# Make prediction
result = predict_image('xray.jpg')
if result:
    print(f"Classification: {result['class']}")
    print(f"Confidence: {result['confidence']:.2f}%")
    print(f"Top 3 predictions:")
    for i, pred in enumerate(result['top_3_predictions'], 1):
        print(f"  {i}. {pred['class']}: {pred['confidence']:.2f}%")
```

### cURL
```bash
# Get info
curl -s http://localhost:5000/api/info | jq

# Make prediction
curl -X POST \
  -F "file=@xray.jpg" \
  http://localhost:5000/api/predict \
  -s | jq

# Health check
curl -s http://localhost:5000/health | jq

# Pretty print
curl -s http://localhost:5000/api/info | jq '.'
```

### Postman
1. Create new POST request: `{{base_url}}/api/predict`
2. Go to Body tab
3. Select "form-data"
4. Add key "file" with type "File"
5. Select image file
6. Send request

---

## Rate Limiting

Currently not implemented. For production, add:
- Requests per IP per minute
- Requests per API key per hour
- Queue for long-running predictions

Example with Flask-Limiter:
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/predict', methods=['POST'])
@limiter.limit("10 per minute")
def api_predict():
    # ... rest of code
```

---

## Performance Metrics

Typical response times:
- Health check: < 10ms
- API info: < 10ms
- Image prediction: 2-5 seconds (GPU), 5-10 seconds (CPU)
- Heatmap generation: 1-3 seconds

---

## Versioning

Current API Version: **1.0.0**

To prepare for future versions:
```
GET /api/v1/predict
GET /api/v2/predict
```

---

## Deprecated Endpoints

None yet.

---

## Support

For API issues:
1. Check `logs/app.log`
2. Verify model file exists: `model/densenet_model.h5`
3. Check system resources (RAM, CPU)
4. Review error message in response

---

**Last Updated**: 2024
**API Status**: Stable