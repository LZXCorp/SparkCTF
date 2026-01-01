# Use a Python 3.12 image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy bot code
COPY telebot.py .

# Run bot
CMD ["python", "telebot.py"]

# EXPOSE ---
# i dont need a exposed port cause users are not connecting to the service. the dockers is just for running the telegram bot

# docker build -t telebot .
# docker run -d --name my-telegram-bot -e BOT_TOKEN=7807928928:AAGBGO9EghimvRvz5OWxyjq8pTzU9THJ5bI telebot

