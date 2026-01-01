FROM ubuntu:25.04

RUN apt update && \
    apt install -y ucspi-tcp-ipv6 cron && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -u 7077 -m pwn

RUN mkdir -p /home/pwn && \
    chown root:pwn /home/pwn && \
    chmod 650 /home/pwn

COPY sparkcli /home/pwn/sparkcli

COPY flag.txt /home/pwn/flag.txt
COPY pin.txt /home/pwn/pin.txt
COPY canary.txt /home/pwn/canary.txt

RUN chown root:root /home/pwn/flag.txt && \
    chown root:root /home/pwn/pin.txt && \
    chown root:root /home/pwn/canary.txt && \
    chmod 644 /home/pwn/flag.txt && \
    chmod 644 /home/pwn/pin.txt && \
    chmod 644 /home/pwn/canary.txt

RUN chmod +x /home/pwn/sparkcli
WORKDIR /home/pwn

EXPOSE 4000

COPY run.sh /opt/run.sh
COPY cleanup /etc/cron.d/bf-cleanup

RUN chown root:root /opt/run.sh && \
    chown root:root /etc/cron.d/bf-cleanup && \
    chmod 740 /opt/run.sh && \
    chmod 640 /etc/cron.d/bf-cleanup

CMD ["/opt/run.sh"]
