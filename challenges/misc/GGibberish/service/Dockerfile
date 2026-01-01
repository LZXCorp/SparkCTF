# Use official slim Python image
FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libasound2-dev \
    portaudio19-dev \
    libportaudiocpp0 \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*


RUN pip install ggwave_python[audio] pyaudio numpy

# Create non-root user
RUN useradd -m ctf

# Switch to the new user
USER ctf
WORKDIR /app

# Copy challenge file into the container
COPY GGibberish.py .


#expose port
EXPOSE 24682

# Default command: run the script
CMD ["python3", "GGibberish.py"]
