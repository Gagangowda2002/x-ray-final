# X-Ray Medical Image Classification System

A production-ready Flask web application for AI-powered medical image classification using deep learning.

## Features

- 🏥 **Medical Image Classification**: Classify X-Ray images into 12 different categories
- 📊 **Grad-CAM Visualization**: View attention heatmaps showing which regions the model focuses on
- 🎯 **12-Class Classification**: Supports multiple fracture types and normal conditions
- 📱 **Responsive UI**: Modern Bootstrap-based interface with drag-and-drop upload
- 🔌 **REST API**: Built-in API endpoints for programmatic access
- 📝 **Logging System**: Comprehensive logging for debugging and monitoring
- ✅ **Input Validation**: File format and size validation
- 🐳 **Docker Support**: Fully containerized for easy deployment
- ⚡ **Production Ready**: WSGI server with proper error handling

## System Architecture

```
app/
├── app.py                    # Main Flask application
├── config.py               # Configuration management
├── logger.py               # Logging setup
├── validation.py           # File validation utilities
├── prediction.py           # ML prediction engine
├── model/
│   ├── densenet_model.h5  # Pre-trained DenseNet model
│   ├── preprocessing.py    # Image preprocessing
│   └── gradcam.py         # Grad-CAM visualization
├── templates/
│   ├── base.html          # Base Bootstrap template
│   ├── index.html         # Upload page
│   ├── result.html        # Results page
│   └── error.html         # Error page
├── static/
│   ├── css/               # Stylesheets
│   ├── uploads/           # User uploaded images
│   └── heatmaps/          # Generated heatmaps
├── logs/                  # Application logs
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose setup
└── README.md            # This file
```

## Supported Fracture Types

The model can classify the following conditions:

1. Avulsion Fracture
2. Comminuted Fracture
3. Fracture Dislocation
4. Greenstick Fracture
5. Hairline Fracture
6. Impacted Fracture
7. Longitudinal Fracture
8. Normal
9. Oblique Fracture
10. Pathological Fracture
11. Spiral Fracture
12. Transverse Fracture

## Installation

### Prerequisites

- Python 3.9+
- pip or conda
- (Optional) Docker & Docker Compose

### Local Setup

1. **Clone/Extract the repository**
```bash
cd x-ray-classification
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Download dataset (Optional)**
If you want to use the NIH Chest X-rays dataset from Kaggle:
```bash
pip install kagglehub
python
```

Then in Python:
```python
import kagglehub
path = kagglehub.dataset_download("nih-chest-xrays/data")
print("Path to dataset files:", path)
```

5. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your settings
```

6. **Run the application**
```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

## Usage

### Web Interface

1. Open the application in your browser (default: `http://localhost:5000`)
2. Upload an X-Ray image (JPG, PNG, GIF, BMP, DICOM - max 16MB)
3. Click "Analyze Image"
4. View results with:
   - Classification label
   - Confidence percentage
   - Original image
   - Grad-CAM heatmap
   - Top 3 predictions

### REST API

The application provides REST API endpoints:

**Get API Information**
```bash
curl http://localhost:5000/api/info
```

**Make a Prediction**
```bash
curl -X POST -F "file=@image.jpg" http://localhost:5000/api/predict
```

Response:
```json
{
  "success": true,
  "class": "Normal",
  "confidence": 95.23,
  "confidence_score": 0.9523,
  "top_3_predictions": [
    {"class": "Normal", "confidence": 95.23},
    {"class": "Hairline Fracture", "confidence": 3.45},
    {"class": "Transverse Fracture", "confidence": 1.32}
  ],
  "probabilities": {...}
}
```

**Health Check**
```bash
curl http://localhost:5000/health
```

## Deployment

### Docker Deployment (Local)

1. **Build and run with Docker Compose**
```bash
docker-compose up --build
```

The application will be available at `http://localhost:5000`

### Deploy to Render

1. **Push to GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/x-ray-classification
git push -u origin main
```

2. **Create a new Web Service on Render**
   - Go to https://render.com
   - Click "Create +" → "Web Service"
   - Connect your GitHub repository
   - Configure the deployment:
     - **Environment**: Docker
     - **Build Command**: Default
     - **Start Command**: Default
   - Set environment variables from `.env.example`
   - Click "Create Web Service"

3. **Monitor Deployment**
   - Render will automatically build and deploy your application
   - View logs in the Render dashboard

### Deploy to Railway

1. **Push to GitHub** (if not already)

2. **Create Project on Railway**
   - Go to https://railway.app
   - Click "New Project" → "Deploy from GitHub"
   - Select your repository
   - Click "Deploy"

3. **Configure Environment Variables**
   - Go to Variables section
   - Add all variables from `.env.example`
   - Set `PYTHON_VERSION=3.11`

4. **Enable Public Network**
   - In Settings, enable "Public Networking"
   - Note the provided railway.app domain

5. **Deploy**
   - Railway will auto-deploy on each push
   - Your app will be available at the provided domain

### Deploy to Heroku (Alternative)

1. **Install Heroku CLI**
```bash
# macOS/Linux
brew tap heroku/brew && brew install heroku

# Windows
choco install heroku-cli
```

2. **Create Procfile** (already provided in example but ensure it exists)
```
web: gunicorn --bind 0.0.0.0:$PORT --workers 4 app:create_app()
```

3. **Deploy**
```bash
heroku login
heroku create your-app-name
heroku config:set SECRET_KEY=your-secret-key
git push heroku main
heroku logs --tail
```

## Configuration

### Application Settings

Edit `config.py` to adjust:

```python
# File upload settings
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'bmp', 'dicom', 'dcm'}

# Model settings
MODEL_PATH = 'model/densenet_model.h5'

# Logging
LOG_LEVEL = 'INFO'
LOG_FILE = 'logs/app.log'

# Session settings
PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
SESSION_COOKIE_SECURE = True
```

### Environment Variables

Create a `.env` file from `.env.example`:
```
FLASK_ENV=production
SECRET_KEY=your-secure-key
LOG_LEVEL=INFO
```

## Logging

Logs are stored in `logs/app.log` with automatic rotation:
- Log level: INFO (configurable)
- Max file size: 10MB
- Backup count: 10 files
- Format: `TIMESTAMP - LOGGER - LEVEL - MESSAGE`

View logs:
```bash
tail -f logs/app.log
```

## Performance Optimization

### For Production

1. **Use production WSGI server**
```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 app:create_app()
```

2. **Enable gzip compression** (configure in reverse proxy)

3. **Set proper environment**
```bash
export FLASK_ENV=production
export FLASK_DEBUG=False
```

4. **Use CDN for static files** (configure in reverse proxy)

5. **Enable session timeout** (already configured)

## Troubleshooting

### Model Not Found
```bash
# Ensure model file exists
ls model/densenet_model.h5

# Also check permission
chmod 644 model/densenet_model.h5
```

### File Upload Issues
- Check `static/uploads/` directory exists and is writable
- Verify `MAX_CONTENT_LENGTH` setting
- Check disk space

### Port Already in Use
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :5000
kill -9 <PID>
```

### TensorFlow/GPU Issues
```bash
# Use CPU-only version
pip install tensorflow-cpu

# Or use specific CUDA version
pip install tensorflow[and-cuda]
```

## API Documentation

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Web interface |
| POST | `/` | Web interface with file upload |
| POST | `/api/predict` | REST API prediction |
| GET | `/api/info` | API information |
| GET | `/health` | Health check |

## Security Considerations

- ✅ File type validation
- ✅ File size limits
- ✅ Secure file naming
- ✅ CSRF protection (Flask-WTF ready)
- ✅ Secure session cookies (HTTPS in production)
- ✅ Error handling without sensitive data leaks
- ✅ Input validation

**For production, additionally:**
- Use HTTPS
- Set secure SECRET_KEY
- Disable debug mode
- Use environment variables
- Implement rate limiting
- Add authentication if needed

## License

MIT License - See LICENSE file for details

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Support

For issues and questions, please open an GitHub issue or contact support.

---

**Built with ❤️ using Flask, TensorFlow, and Bootstrap**