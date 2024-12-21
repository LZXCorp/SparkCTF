FROM ubuntu:24.04
RUN apt-get update
RUN apt-get install -y ucspi-tcp-ipv6 python3

RUN useradd -u 8888 -m pwn
RUN mkdir -p /home/pwn

COPY app.py /home/pwn/app.py
RUN chmod 755 /home/pwn/app.py
RUN chown -R pwn:pwn /home/pwn

EXPOSE 4000

# Option 1: Use python3 explicitly
CMD ["tcpserver", "-t", "50", "-u", "8888", "-g", "8888", "-RHl0", "0.0.0.0", "4000", "python3", "/home/pwn/app.py"]

# Or Option 2: If you prefer direct execution (requires shebang in app.py)
# CMD ["tcpserver", "-t", "50", "-u", "8888", "-g", "8888", "-RHl0", "0.0.0.0", "4000", "/home/pwn/app.py"]
