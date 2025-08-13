import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.exceptions import BadRequest
import requests
from utilities.determine_env import determine_env
from services.get_uv_index import get_uv_index
from config import config

# Load environment variables
from dotenv import load_dotenv

load_dotenv()

# Get environment configuration
env = os.getenv("FLASK_ENV", "development")
app_config = config[env]

# Configure logging based on environment
logging.basicConfig(
    level=getattr(logging, app_config.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

app.config.from_object(app_config)

CORS(app, origins=app_config.ALLOWED_ORIGINS)

logger.info(f"Starting application in {env} mode")


def validate_location_data(data):
    """Validate the required fields in location data"""
    required_fields = ["lat", "lon", "timezone"]
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return False, f"Missing required fields: {', '.join(missing_fields)}"

    if not isinstance(data["lat"], (int, float)) or not -90 <= data["lat"] <= 90:
        return False, "Latitude must be a number between -90 and 90"

    if not isinstance(data["lon"], (int, float)) or not -180 <= data["lon"] <= 180:
        return False, "Longitude must be a number between -180 and 180"

    if not isinstance(data["timezone"], str) or not data["timezone"]:
        return False, "Timezone must be a non-empty string"

    return True, None


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for monitoring"""
    return (
        jsonify(
            {
                "status": "healthy",
                "service": "uv-index-notifier",
                "version": "1.0.0",
                "environment": env,
            }
        ),
        200,
    )


@app.route("/get_uv_data", methods=["POST"])
def get_uv_data():
    """Get UV index data for a given location"""
    try:
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 400

        try:
            data = request.get_json(silent=False)
        except BadRequest as e:
            logger.error(f"Invalid JSON in request: {e}")
            return jsonify({"error": "Invalid JSON format"}), 400

        if not data:
            return jsonify({"error": "Request body cannot be empty"}), 400

        location_data = data.get("data")
        if not location_data:
            return jsonify({"error": "Missing 'data' field in request"}), 400

        is_valid, error_message = validate_location_data(location_data)
        if not is_valid:
            logger.warning(f"Invalid location data: {error_message}")
            return jsonify({"error": error_message}), 400

        logger.info(
            f"Processing UV request for lat: {location_data['lat']}, lon: {location_data['lon']}, timezone: {location_data['timezone']}"
        )

        try:
            result = get_uv_index(location_data)
            if result is None:
                return jsonify({"error": "Failed to retrieve UV index data"}), 500

            logger.info(f"Successfully retrieved UV data for location")
            return jsonify(result), 200

        except Exception as e:
            logger.error(f"Error processing UV request: {str(e)}")
            return (
                jsonify({"error": "Internal server error while processing UV data"}),
                500,
            )

    except Exception as e:
        logger.error(f"Unexpected error in get_uv_data: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"error": "Method not allowed"}), 405


@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    logger.info(
        f"Starting UV Index Notifier service on {app_config.HOST}:{app_config.PORT}"
    )
    app.run(
        host=app_config.HOST,
        port=app_config.PORT,
        debug=app_config.DEBUG,
        threaded=True,
    )
