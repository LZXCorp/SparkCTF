# Solution

1. Need to do some form of socket programming. Following code requires pwntools to be installed:
```py
from pwn import *

context.update(arch='i386',os='linux')

server_ip = "localhost"
con = remote(server_ip,7730)
# REMOVED 1 LINE FROM THE SOLN CODE
con.sendline(data)

con.interactive()
```

> [!IMPORTANT]
> This challenge is flagged as a 0 solve challenge. The full solution will be withheld until further notice.