import logging
import azure.functions as func
import io
from PIL import Image, ImageOps


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("TransformImage function triggered.")

    image_bytes = req.get_body()

    if not image_bytes:
        logging.error("No image data received.")
        return func.HttpResponse("No image data received.", status_code=400)

    try:
        with Image.open(io.BytesIO(image_bytes)) as img:
            img = ImageOps.grayscale(img)

            output = io.BytesIO()
            img.save(output, format="JPEG")
            output.seek(0)

            return func.HttpResponse(output.getvalue(), status_code=200, mimetype="image/jpeg")

    except Exception as e:
        logging.error(f"Error transforming image: {e}")
        return func.HttpResponse(f"Error processing image: {e}", status_code=500)
