FROM python:3.11-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY app.py .
COPY .env .env

# Expose port
EXPOSE 5001

# Run Flask app
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--timeout", "120", "app:app"]
