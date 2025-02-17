# Use a lightweight Python image
FROM python:3.13-slim

# Set up working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create the logs directory
RUN mkdir /app/logs

# Copy application files
COPY app /app

# Run as a non-root user
RUN useradd -m myuser
USER myuser

# Expose port
EXPOSE 5000

# Start the Flask application
CMD ["python", "app.py"]