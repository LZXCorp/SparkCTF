#!/bin/bash

tcpserver -v -u 7077 -g 7077 -RHl0 0.0.0.0 4000 /home/pwn/sparkcli &
cron &

tail -f
