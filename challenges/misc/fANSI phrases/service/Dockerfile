# Python image
FROM python:3.12

# Working directory
WORKDIR /app

# Python script
COPY ctfserver.py flag.txt ./

# Run python server
CMD ["python", "ctfserver.py"]

# Expose a port
EXPOSE 4444
