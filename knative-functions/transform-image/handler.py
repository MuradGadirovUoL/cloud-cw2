from flask import Flask, request, send_file
import io
from PIL import Image, ImageOps
import requests

app = Flask(__name__)

WATERMARK_URL = "http://watermark-image.default.svc.cluster.local"

@app.route("/", methods=["POST"])
def transform():
    if not request.data:
        return "No image received", 400

    img = Image.open(io.BytesIO(request.data))
    gray_img = ImageOps.grayscale(img)

    output = io.BytesIO()
    gray_img.save(output, format="JPEG")
    output.seek(0)

    response = requests.post(WATERMARK_URL, data=output.getvalue())

    return send_file(io.BytesIO(response.content), mimetype="image/jpeg")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)