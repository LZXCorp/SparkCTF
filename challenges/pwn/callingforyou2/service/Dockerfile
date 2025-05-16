FROM ubuntu:24.04

RUN apt-get update
RUN apt-get install -y ucspi-tcp-ipv6 gcc gcc-multilib g++-multilib

RUN useradd -u 8888 -m pwn
RUN mkdir -p /home/pwn
RUN chown -R pwn:pwn /home/pwn

COPY callv2.c /home/pwn/callv2.c
RUN gcc -o /home/pwn/callv2 /home/pwn/callv2.c -no-pie -fno-stack-protector \
    && strip --strip-unneeded /home/pwn/callv2 \
    && rm /home/pwn/callv2.c

COPY flag.txt /home/pwn/flag.txt
RUN chmod 444 /home/pwn/flag.txt

RUN chmod +x /home/pwn/callv2
WORKDIR /home/pwn

EXPOSE 4000

CMD ["tcpserver","-t","50","-u","8888","-g","8888","-RHl0","0.0.0.0","4000","/home/pwn/callv2"]