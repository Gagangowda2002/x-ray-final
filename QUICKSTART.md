# Quick Start Guide

Get the X-Ray Medical Image Classification system up and running in 5 minutes.

## Installation

### 1. Clone/Extract Repository
```bash
cd x-ray-final
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Application
```bash
python app.py
```

The application will start at: **http://localhost:5000**

---

## Quick Docker Setup

### 1. Build and Run
```bash
docker build -t x-ray:latest .
docker run -p 5000:5000 x-ray:latest
```

Access at: **http://localhost:5000**

### 2. Or Use Docker Compose
```bash
docker-compose up --build
```

---

## First Test

1. Open browser: **http://localhost:5000**
2. Upload a chest X-Ray image (JPG, PNG, etc.)
3. Click "Analyze Image"
4. View results with heatmap

---

## API Testing

### Get API Info
```bash
curl http://localhost:5000/api/info
```

### Test Prediction
```bash
curl -X POST -F "file=@image.jpg" http://localhost:5000/api/predict
```

### Health Check
```bash
curl http://localhost:5000/health
```

---

## Next Steps

1. **Configure Environment**: Copy `.env.example` to `.env` and update settings
2. **Review Deployment**: See `DEPLOYMENT.md` for cloud deployment
3. **Clean Up Files**: See `CLEANUP.md` for removing development files
4. **Enable Logging**: Check `logs/app.log` for application logs

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 5000 in use | Kill process: `lsof -i :5000 \| grep LISTEN \| awk '{print $2}' \| xargs kill -9` |
| Module not found | Run: `pip install -r requirements.txt` |
| Model not found | Check `model/densenet_model.h5` exists |
| Permission denied | Run with sudo or check directory permissions |

---

**For detailed documentation, see [README.md](README.md)**