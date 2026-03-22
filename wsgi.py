"""
WSGI entry point for production servers (Gunicorn, etc.)
"""
import os
from app import create_app
from logger import get_logger

# Set environment
env = os.environ.get('FLASK_ENV', 'production')

# Create application
app = create_app(env)

# Get logger
logger = get_logger(__name__)

if __name__ == "__main__":
    logger.info(f"Starting WSGI application in {env} mode")
    app.run()