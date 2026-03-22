# Configuration Guide

Learn how to configure the X-Ray Medical Image Classification system for different environments.

## Quick Configuration

### Development Environment
```.env
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=dev-key-only-for-development
LOG_LEVEL=DEBUG
MAX_CONTENT_LENGTH=16777216
```

### Production Environment
```.env
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=<generate-strong-32-char-key>
LOG_LEVEL=INFO
MAX_CONTENT_LENGTH=16777216
SESSION_COOKIE_SECURE=True
```

---

## Configuration File Reference

### config.py

#### Config Class Variables

```python
# Flask Settings
SECRET_KEY              # Secret key for sessions (32+ chars)
DEBUG                   # Debug mode (True/False)
TESTING                 # Testing mode (True/False)

# File Upload Settings
UPLOAD_FOLDER          # Directory for uploaded images
HEATMAP_FOLDER         # Directory for generated heatmaps
MAX_CONTENT_LENGTH     # Max file size: 16 * 1024 * 1024 (16MB)
ALLOWED_EXTENSIONS     # Allowed file types: {jpg, jpeg, png, ...}

# Model Settings
MODEL_PATH             # Path to DenseNet model

# Logging Settings
LOG_LEVEL              # INFO, DEBUG, WARNING, ERROR
LOG_FILE               # Path to log file

# Session Settings
PERMANENT_SESSION_LIFETIME  # Session timeout duration
SESSION_COOKIE_SECURE       # HTTPS only (True/False)
SESSION_COOKIE_HTTPONLY     # JS access (False = secure)
SESSION_COOKIE_SAMESITE     # CSRF protection
```

---

## Environment Variables

### Required Variables

```bash
# Flask Configuration
FLASK_ENV=development|production|testing
FLASK_APP=app.py

# Security
SECRET_KEY=your-secret-key-minimum-32-characters
```

### Optional Variables

```bash
# Server
SERVER_HOST=0.0.0.0
SERVER_PORT=5000
SERVER_WORKERS=4

# Logging
LOG_LEVEL=DEBUG|INFO|WARNING|ERROR|CRITICAL

# File Upload
MAX_FILE_SIZE_MB=16
ALLOWED_EXTENSIONS=jpg,jpeg,png,gif,bmp,dicom,dcm

# Database (if using)
DATABASE_URL=postgresql://user:pass@localhost/dbname

# Cloud Storage (for backups)
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_BUCKET_NAME=your-bucket
```

---

## Generate Secret Key

### Python
```python
import secrets
print(secrets.token_hex(32))
```

### Command Line
```bash
# Linux/macOS
python3 -c "import secrets; print(secrets.token_hex(32))"

# Windows PowerShell
python -c "import secrets; print(secrets.token_hex(32))"

# Output example: 
# a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4
```

---

## Configuration for Different Environments

### Local Development

```python
# config.py - DevelopmentConfig
DEBUG = True
LOG_LEVEL = 'DEBUG'
SESSION_COOKIE_SECURE = False
TESTING = False
```

**.env file:**
```
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=dev-only-secret
LOG_LEVEL=DEBUG
```

**Run:**
```bash
python app.py
```

### Testing

```python
# config.py - TestingConfig
TESTING = True
WTF_CSRF_ENABLED = False
LOG_LEVEL = 'DEBUG'
```

**.env file:**
```
FLASK_ENV=testing
SECRET_KEY=test-secret
LOG_LEVEL=DEBUG
```

**Run:**
```bash
pytest
```

### Production

```python
# config.py - ProductionConfig
DEBUG = False
LOG_LEVEL = 'INFO'
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
```

**.env file:**
```
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=<strong-32-char-key>
LOG_LEVEL=INFO
SESSION_COOKIE_SECURE=True
```

**Run:**
```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 app:create_app()
```

---

## Django-Style Settings Override

Override any config setting via environment variables:

```python
# In config.py, add at end:
import os
os.environ.get('CUSTOM_SETTING', 'default_value')
```

```bash
# Usage
export CUSTOM_SETTING=custom_value
python app.py
```

---

## Docker Configuration

### Dockerfile Environment
```dockerfile
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1
```

### docker-compose.yml Environment
```yaml
environment:
  - FLASK_ENV=development
  - FLASK_APP=app.py
  - SECRET_KEY=your-secret-key
  - LOG_LEVEL=DEBUG
```

### Build-time Configuration
```bash
docker build \
  --build-arg FLASK_ENV=production \
  -t x-ray:latest .
```

---

## File Upload Configuration

### Allowed Extensions

```python
ALLOWED_EXTENSIONS = {
    'jpg', 'jpeg',  # JPEG images
    'png',          # PNG images
    'gif',          # GIF images
    'bmp',          # Bitmap images
    'dicom', 'dcm'  # DICOM medical images
}
```

To add/remove extensions, modify `config.py`:
```python
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'tiff', 'tif'}
```

### Maximum File Size

Default: 16MB

To change:
```python
# In config.py
MAX_CONTENT_LENGTH = 32 * 1024 * 1024  # 32MB
```

Or via environment:
```bash
export MAX_CONTENT_LENGTH=33554432  # 32MB in bytes
```

---

## Logging Configuration

### Log Levels

```python
# In order of severity:
DEBUG      # 10 - Detailed debugging info
INFO       # 20 - General information
WARNING    # 30 - Warning messages (default)
ERROR      # 40 - Error messages
CRITICAL   # 50 - Critical errors
```

### Log File Location

```python
LOG_FILE = 'logs/app.log'  # Relative to app root
```

To use absolute path:
```python
import os
LOG_FILE = os.path.join('/var/log', 'xray_app.log')
```

### Log Rotation

```python
# In logger.py - RotatingFileHandler
maxBytes=10485760,  # 10MB per file
backupCount=10      # Keep 10 files
```

### Log Format

Current format:
```
2024-01-15 10:30:45 - xray_app - INFO - Message here
```

To customize, modify `logger.py`:
```python
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

---

## Security Configuration

### HTTPS/SSL

```python
# Production settings
SESSION_COOKIE_SECURE = True       # HTTPS only
SESSION_COOKIE_HTTPONLY = True     # No JS access
SESSION_COOKIE_SAMESITE = 'Lax'    # CSRF protection
```

### CORS (if needed)

```python
# Add to app.py
from flask_cors import CORS
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://example.com"],
        "methods": ["POST", "GET"],
        "allow_headers": ["Content-Type"]
    }
})
```

### Rate Limiting

```python
# Add to app.py
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
    pass
```

---

## Performance Tuning

### Gunicorn Workers

```bash
# Formula: (2 x CPU cores) + 1
# For 4-core system:
gunicorn --workers 9 app:create_app()

# For auto-detection:
gunicorn --workers auto app:create_app()
```

### Timeout Settings

```bash
# Default: 30 seconds
gunicorn --timeout 120 app:create_app()
```

### Keep-Alive

```bash
gunicorn --keep-alive 5 app:create_app()
```

---

## Monitoring Configuration

### Application Metrics

```python
# Add to app.py for metrics tracking
from flask import g
import time

@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request
def after_request(response):
    elapsed = time.time() - g.start_time
    logger.info(f"Request: {request.path} - Status: {response.status_code} - Time: {elapsed:.2f}s")
    return response
```

### Health Check Configuration

```python
# Current health check
@app.route('/health', methods=['GET'])
def health():
    return {
        'status': 'healthy',
        'model_loaded': prediction_engine is not None
    }
```

---

## Configuration Checklist

Development:
- [ ] FLASK_ENV=development
- [ ] FLASK_DEBUG=True
- [ ] SECRET_KEY set
- [ ] LOG_LEVEL=DEBUG
- [ ] ALLOWED_EXTENSIONS configured

Staging:
- [ ] FLASK_ENV=production
- [ ] FLASK_DEBUG=False
- [ ] Strong SECRET_KEY
- [ ] LOG_LEVEL=INFO
- [ ] SSL/HTTPS enabled
- [ ] CORS configured

Production:
- [ ] All staging items
- [ ] Monitor logs
- [ ] Backup configured
- [ ] Health checks enabled
- [ ] Rate limiting active
- [ ] Error reporting configured
- [ ] Security headers set
- [ ] Database backups scheduled

---

## Troubleshooting Configuration

### Configuration Not Applied
```bash
# Clear Python cache
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# Restart application
python app.py
```

### Environment Variables Not Found
```bash
# Verify .env file
cat .env

# Load manually
set -a
source .env
set +a

# Verify variable
echo $FLASK_ENV
```

### Model Not Loading
```python
# In config.py, verify:
print(f"Model path: {Config.MODEL_PATH}")
print(f"Exists: {os.path.exists(Config.MODEL_PATH)}")
```

---

**For more help, see [README.md](README.md) and [DEPLOYMENT.md](DEPLOYMENT.md)**