# Use a lightweight official Python runtime as the base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies (e.g., Flask)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the core application files and directories
COPY app.py .
COPY flag.txt .

# Copy the necessary directories for templates and assets
# Flask needs the 'templates' folder
COPY templates/ templates/
COPY assets/ assets/

# Expose the port used by app.py (5001)
EXPOSE 5001

# Define the command to run the application
CMD ["python", "app.py"]
