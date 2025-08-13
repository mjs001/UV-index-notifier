import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration class"""

    DEBUG = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    HOST = os.getenv("FLASK_HOST", "0.0.0.0")
    PORT = int(os.getenv("FLASK_PORT", 5000))

    # CORS Configuration
    ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

    # Request Configuration
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 30))
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    # API URLs
    UV_API_BASE_URL = "https://api.open-meteo.com/v1/forecast"
    TIME_API_BASE_URL = "https://timeapi.io/api/time/current/zone"


class DevelopmentConfig(Config):
    """Development configuration"""

    DEBUG = True
    LOG_LEVEL = "DEBUG"


class ProductionConfig(Config):
    """Production configuration"""

    DEBUG = False
    LOG_LEVEL = "WARNING"


class TestingConfig(Config):
    """Testing configuration"""

    TESTING = True
    DEBUG = True


# Configuration dictionary
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
