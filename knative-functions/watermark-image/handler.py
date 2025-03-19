from flask import Flask, request, send_file
import io
from PIL import Image, ImageDraw, ImageFont
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route("/", methods=["POST"])
def watermark():
    if not request.data:
        logger.error("No image data received")
        return "No image received", 400

    try:
        img = Image.open(io.BytesIO(request.data))
        img = img.convert("RGB")

        draw = ImageDraw.Draw(img)

        text = "Serverless Demo"
        font = ImageFont.load_default()

        left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
        text_width = right - left
        text_height = bottom - top

        margin = 10
        x = img.width - text_width - margin
        y = img.height - text_height - margin

        draw.text((x, y), text, fill=(255, 0, 0), font=font)  # Red text

        output = io.BytesIO()
        img.save(output, format="JPEG")
        output.seek(0)

        return send_file(output, mimetype="image/jpeg")

    except Exception as e:
        logger.error(f"Error processing image: {e}")