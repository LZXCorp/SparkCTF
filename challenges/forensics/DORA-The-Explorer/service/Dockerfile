FROM ubuntu:22.04
RUN apt update && apt install -y apache2
RUN echo "Listen 34598" >> /etc/apache2/ports.conf
RUN sed -i 's/:80/:34598/g' /etc/apache2/sites-available/000-default.conf
COPY index.html /var/www/html/index.html
RUN chmod 644 /var/www/html/index.html
RUN rm -f /var/www/html/index.html.* 
EXPOSE 34598
CMD ["apache2ctl", "-D", "FOREGROUND"]
