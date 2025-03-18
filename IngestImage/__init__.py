import logging
import azure.functions as func
import requests
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("IngestImage function processed a request.")

    # Read the image bytes from request
    image_bytes = req.get_body()
    if not image_bytes:
        return func.HttpResponse("No image data received.", status_code=400)

    # Call TransformImage function
    transform_url = os.getenv("TRANSFORM_URL")
    if not transform_url:
        return func.HttpResponse("TRANSFORM_URL not configured.", status_code=500)

    transform_response = requests.post(transform_url, data=image_bytes)

    if transform_response.status_code != 200:
        return func.HttpResponse(f"Error calling TransformImage: {transform_response.text}", status_code=500)

    # Call WatermarkImage function with transformed image
    watermark_url = os.getenv("WATERMARK_URL")
    if not watermark_url:
        return func.HttpResponse("WATERMARK_URL not configured.", status_code=500)

    watermark_response = requests.post(watermark_url, data=transform_response.content)

    if watermark_response.status_code != 200:
        return func.HttpResponse(f"Error calling WatermarkImage: {watermark_response.text}", status_code=500)

    return func.HttpResponse(watermark_response.content, status_code=200, mimetype="image/jpeg")
