FROM ubuntu:24.04

RUN apt-get update
RUN apt-get install -y ucspi-tcp-ipv6 gcc gcc-multilib g++-multilib

RUN useradd -u 8888 -m pwn
RUN mkdir -p /home/pwn
RUN chown -R pwn:pwn /home/pwn

COPY chall.c /home/pwn/chall.c
RUN gcc -o /home/pwn/chall /home/pwn/chall.c && \
    rm /home/pwn/chall.c

RUN chmod +x /home/pwn/chall

COPY flag.txt /home/pwn/flag.txt
RUN chmod 444 /home/pwn/flag.txt

WORKDIR /home/pwn

EXPOSE 1081

CMD ["tcpserver","-t","50","-u","8888","-g","8888","-RHl0","0.0.0.0","1081","/home/pwn/chall"]
