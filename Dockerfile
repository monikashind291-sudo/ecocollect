# Use official lightweight Python image
FROM python:3.11-slim

# Set environment variables
# Prevents Python from writing .pyc files to disk and enables unbuffered stdout/stderr logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

# Set working directory inside container
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files to container
COPY . .

# Expose default container port
EXPOSE 8080

# Launch application using gunicorn listening on 0.0.0.0 and dynamic $PORT
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 app:app
