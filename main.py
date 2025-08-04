from flask import Flask, request, jsonify
import requests
from werkzeug.exceptions import BadRequest
from utilities.determine_env import determine_env
from services.get_uv_index import get_uv_index


app = Flask(__name__)


@app.route("/get_uv_data", methods=["POST"])  # make sure matches Next
async def get_uv_data():
    try:
        data = request.get_json(silent=False)
    except BadRequest as e:
        return jsonify({"error": str(e.description)})
    processed_data = await jsonify(get_uv_index(data))
    return processed_data


if __name__ == "__main__":
    app.run()
# runs on localhost:5000
