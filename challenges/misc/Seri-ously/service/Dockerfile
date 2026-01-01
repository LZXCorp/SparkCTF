# Use official slim Python image
FROM python:3.10-slim



# Create non-root user
RUN useradd -m ctf

# Switch to the new user
USER ctf
WORKDIR /app

# Copy challenge file into the container
COPY serialization.py .



#expose port
EXPOSE 24681

# Default command: run the script
CMD ["python3", "serialization.py"]
