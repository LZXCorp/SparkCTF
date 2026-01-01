FROM ubuntu:24.04

# Install cron and gcc for compiling the viewer binary
RUN apt-get update && apt-get install -y cron gcc python3-pip python-is-python3 sudo && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Create flagviewer user for SUID binary
RUN groupadd -r flagviewer && useradd -r -g flagviewer flagviewer

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt --break-system-packages

# Create directory for summaries and set proper permissions
RUN mkdir -p /tmp/summaries && \
    chown -R appuser:appuser /app /tmp/summaries && \
    chmod -R 755 /app && \
    chmod -R 777 /tmp/summaries

# Add CTF flag here and set permissions so only flagviewer can read it
COPY flag.txt /app/flag.txt
RUN chown flagviewer:flagviewer /app/flag.txt && \
    chmod 400 /app/flag.txt

# Copy viewer source and compile the SUID binary
COPY viewer.c /app/viewer.c
RUN gcc -o /app/viewer /app/viewer.c && \
    chown flagviewer:flagviewer /app/viewer && \
    chmod 4755 /app/viewer && \
    rm /app/viewer.c

# Copy and setup cron job
COPY cleanup-cron /etc/cron.d/cleanup-cron
RUN chmod 0644 /etc/cron.d/cleanup-cron && \
    crontab /etc/cron.d/cleanup-cron && \
    touch /var/log/cron.log

# Add sudoers file
COPY sudoersfile /etc/sudoers

# Copy startup script
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Remove additional copies from the /app folder
RUN rm /app/sudoersfile /app/Dockerfile /app/docker-entrypoint.sh /app/cleanup-cron


EXPOSE 8550

# Use entrypoint script to start both cron and gunicorn
ENTRYPOINT ["/docker-entrypoint.sh"]
