from pwn import *
from time import time
from ctypes import CDLL

p = remote("0.0.0.0", 1081)

# use the same lib for the same PRNG
libc = CDLL('/lib/x86_64-linux-gnu/libc.so.6')

# use the same seed (current time)
seed = int(time())

# use libc srand function to get same PRNG values
libc.srand(seed)
    
for i in range(10):

    # use the same guess
    guess = libc.rand() % 6 + 1  
    
    p.recvuntil("Make your guess (1-6):\n")
    
    p.sendline(str(guess))

p.recvuntil("Correct!\n\n")
print(p.recvall().decode())