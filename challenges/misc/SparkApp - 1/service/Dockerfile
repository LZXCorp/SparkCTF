FROM php:8.1-apache

# Set environment variable
ENV APACHE_DOCUMENT_ROOT=/var/www/html

# Copy application files
COPY ./appcode/ /var/www/html/

# copy them keys
COPY ./server.crt /var/www/html/
COPY ./server.key /var/www/html/

# Expose port 8443 for HTTPS
EXPOSE 8443

# Expose port 8080 for HTTP
EXPOSE 8080

# Configure Apache and start the server
COPY ./ports.conf /etc/apache2/ports.conf
COPY ./ssl-site.conf /etc/apache2/sites-available/ssl-site.conf

RUN a2enmod ssl && \
    a2enmod headers && \
    a2ensite ssl-site

# Start Apache in foreground
CMD ["apache2-foreground"]
