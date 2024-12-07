# Flask application Dockerfile
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy application files
COPY . /app

# Copy dataset files
COPY base/static/adminResources/dataset /app/base/static/adminResources/dataset

# Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your app will run on
EXPOSE 5671

# Start the application
CMD ["python", "app.py"]