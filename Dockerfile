FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install shared dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose default port (optional)
EXPOSE 8000