from flask import Flask, request, send_file
import io
from PIL import Image, ImageDraw, ImageFont
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route("/", methods=["POST"])
def watermark():
    # Check if image data is present
    if not request.data:
        logger.error("No image data received")
        return "No image received", 400

    try:
        img = Image.open(io.BytesIO(request.data))
        img = img.convert("RGB")

        # Create a drawing context
        draw = ImageDraw.Draw(img)

        # Define the watermark text and font
        text = "Serverless Demo"
        font = ImageFont.load_default()  # Use the default font

        # Calculate the bounding box of the text
        left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
        text_width = right - left
        text_height = bottom - top

        # Calculate the position for the watermark (bottom-right corner with margin)
        margin = 10
        x = img.width - text_width - margin
        y = img.height - text_height - margin

        # Add the watermark
        draw.text((x, y), text, fill=(255, 0, 0), font=font)  # Red text

        # Save the watermarked image to a BytesIO object
        output = io.BytesIO()
        img.save(output, format="JPEG")
        output.seek(0)

        return send_file(output, mimetype="image/jpeg")

    except Exception as e:
        logger.error(f"Error processing image: {e}")