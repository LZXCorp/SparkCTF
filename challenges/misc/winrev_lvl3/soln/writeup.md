# winrev_lvl3 - CTF Writeup

## Challenge Overview
This is an advanced Windows reverse engineering challenge that involves analyzing a cryptographic implementation. Participants are provided with:
1. A Windows executable (`winrev_lvl3.exe`) that implements AES-256 encryption
2. An encrypted file (`flag.txt.enc`) containing the flag

The goal is to reverse engineer the encryption process and decrypt the file to obtain the flag.

## Initial Analysis

The challenge provides two files:
- `winrev_lvl3.exe` - The encryption binary
- `flag.txt.enc` - The encrypted flag file

Running the executable alone won't directly reveal the flag. Instead, we need to understand how the encryption works and reverse the process.

## Reverse Engineering with Ghidra

Loading the binary into Ghidra (or IDA Pro/Binary Ninja) reveals the encryption implementation using Windows Cryptography API Next Generation (CNG).

### Key Findings

Upon decompiling the binary, we can identify several critical pieces of information:

1. **Cryptographic Algorithm:** The binary uses AES-256-CBC (Advanced Encryption Standard with 256-bit key in Cipher Block Chaining mode)

2. **Windows CNG API Usage:** The binary makes calls to BCrypt* functions:
   - `BCryptOpenAlgorithmProvider()` - Opens AES algorithm provider
   - `BCryptSetProperty()` - Sets chaining mode to CBC
   - `BCryptGenerateSymmetricKey()` - Creates encryption key
   - `BCryptEncrypt()` - Performs the encryption

3. **Key Discovery:** The encryption key is hardcoded in the binary but obfuscated using XOR encoding
   - XOR key: `0x5A`
   - Encoded string in binary: `"averyinterestingexampleasicanrev"`
   - After XOR decoding with `0x5A`, the actual key is: `aebUfihAbUbZAihlbgdtz\x7fbdZiadhUbe`

4. **Initialization Vector (IV):** The IV is set to 16 bytes of zeros (`\x00` * 16)

5. **Padding Scheme:** PKCS7 padding is applied to ensure data is a multiple of the AES block size (16 bytes)

### Analyzing the Encryption Function

The decompiled code reveals the encryption process:

```cpp
// Simplified pseudocode from reverse engineering
1. Open AES algorithm provider
2. Set chaining mode to CBC
3. XOR-decode the hardcoded key (0x5A XOR operation)
4. Generate symmetric key object from decoded key
5. Initialize IV with 16 zero bytes
6. Apply PKCS7 padding to plaintext
7. Encrypt using AES-256-CBC
8. Write encrypted data to .enc file
```

### Critical Code Observations

- **Key Obfuscation (XOR with 0x5A):**
  ```
  Original (visible in binary): "averyinterestingexampleasicanrev"
  After XOR with 0x5A:          "aebUfihAbUbZAihlbgdtz\x7fbdZiadhUbe"
  ```

- **Padding Implementation:**
  ```cpp
  padding_length = 16 - (plaintext_size % 16)
  for (i = 0; i < padding_length; i++)
      padded_data[plaintext_size + i] = padding_length
  ```

## Decryption Strategy

To decrypt the flag file, we need to:
1. Extract the AES-256 key (after XOR decoding)
2. Use the same IV (16 zero bytes)
3. Decrypt using AES-256-CBC
4. Remove PKCS7 padding
5. Read the plaintext flag

### Solution: Using the Provided Python Script

A Python decryption script (`decrypt.py`) is provided in the solution folder:

**Step 1:** Ensure you have the required Python library:

```bash
pip install cryptography
```

Or install from requirements.txt:

```bash
pip install -r requirements.txt
```

**Step 2:** Run the decryption script:

```bash
python decrypt.py flag.txt.enc
```

**Output:**

```
============================================================
  AES-256 Decryption Tool for winrev_lvl3.exe
============================================================

Input file:  flag.txt.enc
Output file: flag.txt

[*] Starting decryption process...

[*] Reading encrypted file: flag.txt.enc
[*] Encrypted data size: 48 bytes
[*] Initializing AES-256-CBC cipher...
[*] Decrypting...
[*] Decrypted data size (with padding): 48 bytes
[*] Removing PKCS7 padding...
[*] Final decrypted data size: 38 bytes
[*] Writing decrypted file: flag.txt

============================================================
[SUCCESS] File decrypted successfully!
============================================================

File Information:
  Encrypted file:  flag.txt.enc (48 bytes)
  Decrypted file:  flag.txt (38 bytes)
  Padding removed: 10 bytes
```

**Step 3:** Read the decrypted flag:

```bash
cat flag.txt
```

**Output:**

```
SPARK{@dv@nc3d_3ncryp710n_r3v3r53r}
```

### Manual Decryption (Alternative Method)

If you prefer to write your own decryption script, here's a minimal Python example:

```python
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Extracted from reverse engineering
AES_KEY = b'aebUfihAbUbZAihlbgdtz\x7fbdZiadhUbe'
IV = b'\x00' * 16

# Read encrypted file
with open('flag.txt.enc', 'rb') as f:
    ciphertext = f.read()

# Create AES-256-CBC cipher
cipher = Cipher(algorithms.AES(AES_KEY), modes.CBC(IV), backend=default_backend())
decryptor = cipher.decryptor()

# Decrypt
padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

# Remove PKCS7 padding
padding_length = padded_plaintext[-1]
plaintext = padded_plaintext[:-padding_length]

# Display flag
print(plaintext.decode('utf-8'))
```

## Learning Points

This challenge demonstrates:
1. **Cryptographic API Analysis:** Understanding Windows CNG API and its function calls
2. **Algorithm Identification:** Recognizing AES-256-CBC implementation from decompiled code
3. **Key Extraction:** Finding and decoding obfuscated encryption keys (XOR operations)
4. **Parameter Discovery:** Identifying cryptographic parameters (IV, padding scheme)
5. **Implementation Reversal:** Translating encryption logic into working decryption code
6. **Cryptography Fundamentals:** Understanding block ciphers, modes of operation, and padding

## Tools Used
- Ghidra / IDA Pro / Binary Ninja (for static analysis)
- Python 3 with `cryptography` library (for decryption)
- Windows environment (optional, for running the executable)

## Technical Details

### Cryptographic Parameters
- **Algorithm:** AES (Advanced Encryption Standard)
- **Key Size:** 256 bits (32 bytes)
- **Mode:** CBC (Cipher Block Chaining)
- **IV:** 16 bytes of zeros
- **Padding:** PKCS7
- **Block Size:** 16 bytes (128 bits)

### Key Extraction Process
1. Locate hardcoded string in binary: `"averyinterestingexampleasicanrev"`
2. Identify XOR operation with constant `0x5A`
3. Apply XOR to each byte:
   ```
   'a' ^ 0x5A = 0x61 ^ 0x5A = 0x3B = 'e'
   'v' ^ 0x5A = 0x76 ^ 0x5A = 0x2C = ...
   (continue for all 32 bytes)
   ```
4. Result: `aebUfihAbUbZAihlbgdtz\x7fbdZiadhUbe`

### Windows CNG API Functions Observed
- `BCryptOpenAlgorithmProvider()` - Initialize crypto provider
- `BCryptSetProperty()` - Configure encryption parameters
- `BCryptGenerateSymmetricKey()` - Create key object
- `BCryptEncrypt()` - Perform encryption
- `BCryptDestroyKey()` - Clean up key object
- `BCryptCloseAlgorithmProvider()` - Clean up provider

## Flag
`SPARK{@dv@nc3d_3ncryp710n_r3v3r53r}`
