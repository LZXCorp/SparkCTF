FROM ubuntu:24.04
RUN apt-get update
RUN apt-get install -y ucspi-tcp-ipv6 gcc gcc-multilib g++-multilib

RUN useradd -u 8888 -m pwn
RUN mkdir -p /home/pwn
RUN chown -R pwn:pwn /home/pwn

ADD source.c /home/pwn/source.c
RUN gcc -m32 -o /home/pwn/fmt_yallz /home/pwn/source.c -fno-stack-protector -z execstack

RUN chmod +x /home/pwn/fmt_yallz
WORKDIR /home/pwn

EXPOSE 4000

CMD ["tcpserver","-t","50","-u","8888","-g","8888","-RHl0","0.0.0.0","4000","/home/pwn/fmt_yallz"]