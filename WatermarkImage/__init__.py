import logging
import azure.functions as func
import io
from PIL import Image, ImageDraw, ImageFont
import os

def load_font():
    font_path = "arial.ttf"
    font_size = 40
    try:
        if os.path.exists(font_path):
            return ImageFont.truetype(font_path, font_size)
        return ImageFont.load_default()
    except Exception:
        return ImageFont.load_default()

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("WatermarkImage function triggered.")

    image_bytes = req.get_body()
    if not image_bytes:
        return func.HttpResponse("No image data received.", status_code=400)

    try:
        with Image.open(io.BytesIO(image_bytes)) as img:
            img = img.convert("RGB")
            draw = ImageDraw.Draw(img)
            font = load_font()

            bbox = draw.textbbox((0, 0), "Serverless Demo", font=font)
            x, y = img.width - bbox[2] - 10, img.height - bbox[3] - 10

            draw.rectangle([(x - 5, y - 5), (x + bbox[2] + 5, y + bbox[3] + 5)], fill=(0, 0, 0, 120))
            draw.text((x, y), "Serverless Demo", fill=(255, 255, 255), font=font)

            output = io.BytesIO()
            img.save(output, format="JPEG")
            return func.HttpResponse(output.getvalue(), status_code=200, mimetype="image/jpeg")
    except Exception as e:
        logging.error(f"Error watermarking image: {e}")
        return func.HttpResponse(str(e), status_code=500)
