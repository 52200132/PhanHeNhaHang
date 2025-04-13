FROM base-backend-image:latest

# Set working directory
WORKDIR /app

# Install Python dependencies for SQL Server
RUN pip install --no-cache-dir pyodbc aioodbc

# Copy application code
COPY . .

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
