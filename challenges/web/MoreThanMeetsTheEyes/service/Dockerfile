# Use a small Python base
FROM python:3.11-slim

# Keep Python output unbuffered and avoid .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Working directory inside the container
WORKDIR /app

# Install minimal system packages (for network & pip)
RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy application code
COPY MoreThanMeetsTheEyes.py .

# Install Python dependencies directly
RUN pip install --no-cache-dir Flask gunicorn	

# Expose the port your app uses
EXPOSE 24680

CMD ["python", "MoreThanMeetsTheEyes.py"]