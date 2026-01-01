#!/usr/bin/env python3

def t1(data, key):
    """Transform 1: XOR with key, then nibble swap"""
    result = bytearray(data)
    klen = len(key)
    for i in range(len(result)):
        result[i] ^= key[i % klen]
        result[i] = ((result[i] & 0x0F) << 4) | ((result[i] & 0xF0) >> 4)
    return bytes(result)

def t2(data, key):
    """Transform 2: XOR with reversed key, then NOT"""
    result = bytearray(data)
    klen = len(key)
    dlen = len(result)
    for i in range(dlen):
        result[i] ^= key[(dlen - i - 1) % klen]
        result[i] = (~result[i]) & 0xFF
    return bytes(result)

def t3(data):
    """Transform 3: Rotate left by 3 bits"""
    result = bytearray(data)
    for i in range(len(result)):
        result[i] = ((result[i] << 3) | (result[i] >> 5)) & 0xFF
    return bytes(result)

# Original flag
flag = b"SPARK{w04h_y0uR3_g3tt1ng_th3_h4nG_0f_R3V}"

# Keys
k1 = bytes([0xde, 0xad, 0xbe, 0xef, 0xca])
k2 = bytes([0xfe, 0xba, 0xbe, 0x13, 0x37])

print(f"Original flag: {flag.decode()}")
print(f"Length: {len(flag)}")

# Apply transformations in order
encoded = t1(flag, k1)
print(f"\nAfter t1: {encoded.hex()}")

encoded = t2(encoded, k2)
print(f"After t2: {encoded.hex()}")

encoded = t3(encoded)
print(f"After t3: {encoded.hex()}")

# Split into chunks of 5 (last chunk may be smaller)
chunk_size = 5
chunks = [encoded[i:i+chunk_size] for i in range(0, len(encoded), chunk_size)]

print("\n// C array declarations:")
for idx, chunk in enumerate(chunks, 1):
    hex_str = ', '.join([f'0x{b:02x}' for b in chunk])
    print(f"static unsigned char d{idx}[] = {{{hex_str}}};")

print("\n// Verification - decode back:")
# Reverse the process
decoded = bytearray(encoded)

# Reverse t3
for i in range(len(decoded)):
    decoded[i] = ((decoded[i] >> 3) | (decoded[i] << 5)) & 0xFF

# Reverse t2
dlen = len(decoded)
for i in range(dlen):
    decoded[i] = (~decoded[i]) & 0xFF
    decoded[i] ^= k2[(dlen - i - 1) % len(k2)]

# Reverse t1
for i in range(len(decoded)):
    decoded[i] = ((decoded[i] & 0x0F) << 4) | ((decoded[i] & 0xF0) >> 4)
    decoded[i] ^= k1[i % len(k1)]

print(f"Decoded: {bytes(decoded).decode()}")
print(f"Match: {bytes(decoded) == flag}")
