# winrev_lvl2 - CTF Writeup

## Challenge Overview
This is an intermediate Windows reverse engineering challenge that involves analyzing network communication. The binary requires a specific server interaction to reveal the flag.

## Initial Analysis

Running the binary shows that it attempts to establish a network connection. Without the proper server setup, the binary will fail to reveal the flag.

## Reverse Engineering with Ghidra

Loading the binary into Ghidra (or your preferred disassembler) reveals network-related Windows API calls and string comparisons.

### Key Findings

Upon decompiling the binary, we can identify several important pieces of information:

1. **Network Communication:** The binary uses Windows Socket API (Winsock) functions to establish a TCP connection
2. **Connection Details:**
   - Target host: `127.0.0.1` (localhost)
   - Port: `61187`
3. **Protocol Analysis:** The binary expects to receive a specific message from the server before sending back the flag

### String Discovery

Through static analysis, we can identify a hardcoded string that the binary expects to receive:

```
give me the flag please?
```

The binary performs a string comparison on the received data. If the incoming message matches this exact phrase, it proceeds to send the flag back to the server.

## Getting the Flag

Based on our analysis, we need to create a server that:
1. Listens on TCP port 61187
2. Accepts the connection from the binary
3. Sends the magic phrase: `"give me the flag please?"`
4. Receives and displays the flag

### Solution Method 1: Using the Provided Python Script

A Python script (`flag_server.py`) is provided in the solution folder that automates this process:

**Step 1:** Start the flag server:

```bash
python flag_server.py
```

The server will start listening on `127.0.0.1:61187`.

**Step 2:** In another terminal or command prompt, run the binary:

```bash
winrev_lvl2.exe
```

**Step 3:** The server will automatically:
- Accept the connection from the binary
- Send the magic phrase
- Receive and display the flag

**Output:**

```
[*] CTF Flag Server - Level 2
[*] ========================================
[*] Starting server on 127.0.0.1:61187
[+] Server is listening on 127.0.0.1:61187
[*] Waiting for challenge binary to connect...
[*] (Run winrev_lvl2.exe now)

[+] Connection received from 127.0.0.1:xxxxx
[*] Sending magic phrase: 'give me the flag please?'
[*] Magic phrase sent successfully!
[*] Waiting for flag response from binary...

[+] ========================================
[+] FLAG CAPTURED!
[+] ========================================
[+] SPARK{tcp_r3v3rs3_3ng1n33r_2025!}
[+] ========================================
```

### Solution Method 2: Using netcat

Alternatively, you can use netcat to manually interact with the binary:

**Step 1:** Start a netcat listener:

```bash
nc -lvp 61187
```

**Step 2:** Run the binary in another terminal:

```bash
winrev_lvl2.exe
```

**Step 3:** When the connection is established, type the magic phrase:

```
give me the flag please?
```

**Step 4:** The binary will respond with the flag:

```
SPARK{tcp_r3v3rs3_3ng1n33r_2025!}
```

## Learning Points

This challenge demonstrates:
1. **Network Protocol Analysis:** Understanding how binaries communicate over TCP/IP
2. **Windows Socket API:** Recognizing Winsock function calls (WSAStartup, socket, connect, send, recv)
3. **Dynamic Analysis:** Setting up controlled environments to interact with network-enabled binaries
4. **String Comparison Logic:** Identifying hardcoded strings that trigger specific program behavior
5. **Client-Server Architecture:** Understanding how binaries can act as network clients

## Tools Used
- Ghidra / IDA Pro / Binary Ninja / x64dbg (for static analysis)
- Python 3 with socket library (for server implementation)
- netcat (alternative solution)
- Windows environment (for running the executable)

## Technical Details

### Network Flow
1. Binary initiates TCP connection to 127.0.0.1:61187
2. Server sends: `"give me the flag please?"`
3. Binary validates the received message
4. If validation succeeds, binary sends back the flag
5. Connection closes

### Key Windows API Functions Used
- `WSAStartup()` - Initialize Winsock
- `socket()` - Create socket
- `connect()` - Connect to server
- `recv()` - Receive data
- `send()` - Send data
- `closesocket()` - Close connection

## Flag
`SPARK{tcp_r3v3rs3_3ng1n33r_2025!}`
