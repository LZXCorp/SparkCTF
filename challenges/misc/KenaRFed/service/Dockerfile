FROM ubuntu:24.04
RUN apt-get update
RUN apt-get install -y openssh-server

RUN useradd -u 8888 -m ctf
RUN echo 'ctf:thisisasecret' | chpasswd
RUN mkdir -p /home/ctf
RUN chown -R ctf:ctf /home/ctf
ADD flag.txt /var/log/flag.txt
RUN chmod 644 /var/log/flag.txt
ADD sshd_config /etc/ssh/sshd_config
RUN mkdir -p /run/sshd

EXPOSE 4000

RUN rm -rf /usr/bin/cat /usr/bin/ls /usr/bin/more /usr/bin/less /usr/bin/tail /usr/bin/head /usr/bin/find /usr/bin/tac /usr/bin/nl /usr/bin/grep /usr/bin/apt /usr/bin/apt-get
CMD ["/usr/sbin/sshd","-D","-p","4000"]