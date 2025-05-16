FROM ubuntu:24.04

RUN apt-get update
RUN apt-get install -y ucspi-tcp-ipv6 gcc gcc-multilib g++-multilib

RUN useradd -u 8888 -m pwn
RUN mkdir -p /home/pwn
RUN chown -R pwn:pwn /home/pwn

COPY sparkconsole.c /home/pwn/sparkconsole.c
RUN gcc -m32 -o /home/pwn/sparkconsole /home/pwn/sparkconsole.c -fno-stack-protector && \
    rm /home/pwn/sparkconsole.c

COPY flag.txt /home/pwn/flag.txt
RUN chmod 444 /home/pwn/flag.txt

RUN chmod 511 /home/pwn/sparkconsole
WORKDIR /home/pwn

EXPOSE 4000

CMD ["tcpserver","-t","50","-u","8888","-g","8888","-RHl0","0.0.0.0","4000","/home/pwn/sparkconsole"]