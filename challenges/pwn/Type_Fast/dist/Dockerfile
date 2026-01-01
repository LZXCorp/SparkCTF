FROM ubuntu:24.04

# Install required packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ucspi-tcp gcc make ca-certificates libc6-dev && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -u 8888 -m -s /bin/bash pwn && \
    mkdir -p /home/pwn && \
    chown -R pwn:pwn /home/pwn

COPY chall.c /home/pwn/chall.c
COPY flag.txt /home/pwn/flag.txt

RUN gcc /home/pwn/chall.c -o /home/pwn/chall -fno-stack-protector -no-pie -z execstack && \
    rm /home/pwn/chall.c

RUN chown pwn:pwn /home/pwn/chall && chmod 755 /home/pwn/chall
RUN chmod 444 /home/pwn/flag.txt

WORKDIR /home/pwn

EXPOSE 1067

CMD ["tcpserver","-v","0.0.0.0","1067","/home/pwn/chall"]
