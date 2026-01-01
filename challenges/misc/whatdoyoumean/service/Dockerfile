FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy application files
COPY server.py .
COPY flag.txt .

# Expose the port
EXPOSE 8551

# Run the server
CMD ["python3", "server.py"]
