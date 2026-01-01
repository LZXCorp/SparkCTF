# LinRev Level 3 - CTF Challenge

## Overview
This is a Linux reverse engineering challenge where participants must understand the binary's behavior and extract the hidden flag.

## Challenge Description
The binary performs the following operations:
- Connects to a network service on TCP port 56441 (localhost)
- Implements a specific handshake protocol
- Sends the flag only if all protocol steps are successful
- If any condition fails, prints: "This is just outright insane. Take your time on this!"

## Protocol Flow
1. Binary connects to server on port 56441
2. Server must respond with: `hello linrev3`
3. Binary sends: `sendflagoverthenet?`
4. Server must respond with: `yes`
5. Binary decodes and sends the flag

## Obfuscation Techniques
The flag `SPARK{w04h_y0uR3_g3tt1ng_th3_h4nG_0f_R3V}` is heavily obfuscated using:
- Multi-layer XOR encryption with rotating keys
- Bit manipulation (nibble swapping)
- Byte rotation (bit shifting)
- Split storage across multiple arrays
- NOT operations for additional scrambling

The flag cannot be found using:
- `strings challenge`
- `hexdump -C challenge | grep SPARK`
- Simple pattern matching in hex editors

## Files
- `challenge.c` - Source code for the challenge binary
- `challenge` - Compiled binary (CTF artifact)
- `encode_flag.py` - Helper script that generates obfuscated byte arrays
- `test_server.py` - Test server for verifying the binary

## Building
```bash
gcc -o challenge challenge.c -Wall
```

## Testing
Terminal 1 - Start the test server:
```bash
python3 test_server.py
```

Terminal 2 - Run the challenge binary:
```bash
./challenge
```

If successful, the server will receive and display the flag.

## Solution Approach
Participants can solve this challenge by:
1. **Static Analysis**: Reverse engineer the binary to understand the deobfuscation algorithm
2. **Dynamic Analysis**: Set up a listening server and capture the network traffic
3. **Debugging**: Use GDB to trace execution and examine memory at runtime
4. **Network Interception**: Use tools like `nc` or `socat` to intercept the flag

## Example Server (For Solution)
```python
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 56441))
server.listen(1)
conn, _ = server.accept()

conn.send(b"hello linrev3")
print(conn.recv(1024).decode())  # Receives: sendflagoverthenet?
conn.send(b"yes")
flag = conn.recv(1024).decode()
print(f"Flag: {flag}")
conn.close()
```

## Flag
`SPARK{w04h_y0uR3_g3tt1ng_th3_h4nG_0f_R3V}`
