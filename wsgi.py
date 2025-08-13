import os
from app import app
from config import config

# Get environment configuration
env = os.getenv("FLASK_ENV", "development")
app.config.from_object(config[env])

if __name__ == "__main__":
    app.run()
