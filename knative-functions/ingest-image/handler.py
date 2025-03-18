from flask import Flask, request, send_file
import requests
import io
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TRANSFORM_URL = "http://transform-image.default.svc.cluster.local"

@app.route("/start-process", methods=["POST"])
def ingest():
    if not request.data:
        logger.error("No image data received")
        return "No image received", 400

    try:
        # Send image data to the transform service
        response = requests.post(TRANSFORM_URL, data=request.data, timeout=10)  # 10-second timeout

        # Check if the transform service returned an error
        if response.status_code != 200:
            logger.error(f"Transform service returned status code: {response.status_code}")
            return "Error in transform-image", 500

        # Return the transformed image
        return send_file(io.BytesIO(response.content), mimetype="image/jpeg")

    except requests.exceptions.RequestException as e:
        logger.error(f"Error calling transform service: {e}")
        return "Internal server error", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)