# Cryptography Challenge - Solution Writeup

## Challenge Overview

This challenge involves a custom XOR-based encryption scheme where we need to decrypt an encrypted flag file using cryptanalysis and known plaintext attack.

## Given Files

- `sample.txt` - Known plaintext sample
- `sample.txt.enc` - Encrypted version of sample.txt
- `flag.txt.enc` - Encrypted flag file (target)

## Analysis

### Step 1: Key Recovery from Known Plaintext

By XORing the known plaintext (`sample.txt`) with its encrypted version (`sample.txt.enc`), we can recover the encryption key:

```
Key = Plaintext ⊕ Ciphertext
```

This works because in XOR encryption:
```
Ciphertext = Plaintext ⊕ Key
Therefore: Plaintext ⊕ Ciphertext = Plaintext ⊕ (Plaintext ⊕ Key) = Key
```

### Step 2: Key Structure Discovery

After recovering the key from the sample files, we can observe the following properties:

1. **Key Length**: The key length equals the size of the encrypted data
2. **Key Pattern**:
   - The first byte is randomly generated (changes on each encryption)
   - Each subsequent byte increments by 1 from the previous byte

**Example Key Structure:**
```
If first byte = 0x42
Then key = [0x42, 0x43, 0x44, 0x45, 0x46, ...]
```

This is a weak encryption scheme because the key is predictable once the first byte is known.

### Step 3: Known Plaintext Attack on Flag

We know that the flag starts with `SPARK`. Using this knowledge:

1. Take the first byte of `flag.txt.enc`
2. XOR it with the ASCII value of 'S' (0x53)
3. This reveals the first byte of the key

```python
first_key_byte = encrypted_flag[0] ^ ord('S')
```

### Step 4: Key Generation

Once we have the first byte of the key, we can generate the entire key:

```python
key_length = len(encrypted_flag)
key = [(first_key_byte + i) % 256 for i in range(key_length)]
```

### Step 5: Decryption

Finally, XOR the encrypted flag with the generated key to obtain the plaintext flag:

```python
flag = bytes([encrypted_flag[i] ^ key[i] for i in range(len(encrypted_flag))])
```

## Solution Script

```python
# Read the encrypted flag
with open('flag.txt.enc', 'rb') as f:
    encrypted_flag = f.read()

# Known plaintext attack: flag starts with "SPARK"
first_key_byte = encrypted_flag[0] ^ ord('S')

# Generate the full key (incrementing pattern)
key = bytes([(first_key_byte + i) % 256 for i in range(len(encrypted_flag))])

# Decrypt the flag
flag = bytes([encrypted_flag[i] ^ key[i] for i in range(len(encrypted_flag))])

print(flag.decode())
```
