FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy files
COPY handler.py .
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Use Gunicorn as the production server
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "handler:app"]