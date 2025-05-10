# Solution

1. Need to do some form of socket programming. Following code requires pwntools to be installed:
```py
#!/usr/bin/python3

from pwn import *

server_ip = "localhost"

conn = remote(server_ip,7731)

data = asm('nop') * 128000
conn.sendline(data)
print(conn.recvuntil(b'}'))
```