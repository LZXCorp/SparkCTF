FROM ubuntu:24.04

RUN apt-get update
RUN apt-get install -y ucspi-tcp-ipv6 gcc gcc-multilib g++-multilib

RUN useradd -u 8888 -m pwn
RUN mkdir -p /home/pwn
RUN chown -R pwn:pwn /home/pwn

COPY purpleman.c /home/pwn/purpleman.c
RUN gcc -o /home/pwn/purpleman /home/pwn/purpleman.c -no-pie -fno-stack-protector -z execstack && \
    rm /home/pwn/purpleman.c

COPY flag.txt /home/pwn/flag.txt
RUN chmod 444 /home/pwn/flag.txt

RUN chmod 511 /home/pwn/purpleman
WORKDIR /home/pwn

EXPOSE 4000

CMD ["tcpserver","-t","50","-u","8888","-g","8888","-RHl0","0.0.0.0","4000","/home/pwn/purpleman"]