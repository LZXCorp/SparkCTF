#!/usr/bin/env python3
"""
AES-256 Decryption Tool for winrev_lvl3.exe
Decrypts files encrypted by the winrev_lvl3 application

This script mirrors the encryption logic from main.cpp:
- Algorithm: AES-256-CBC
- Key: "averyinterestingexampleasicanrev" (32 bytes)
- IV: 16 bytes of zeros
- Padding: PKCS7

Usage: python decrypt.py <encrypted_file.enc>
"""

import sys
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# The AES-256 key used by winrev_lvl3.exe
# This key is XOR-encoded in the binary with key 0x5A, but we've decoded it
# NOTE: The comment in main.cpp is misleading! The actual decoded key is below:
AES_KEY = b'aebUfihAbUbZAihlbgdtz\x7fbdZiadhUbe'

# IV (Initialization Vector) - all zeros as used in main.cpp (line 119)
IV = b'\x00' * 16

def remove_pkcs7_padding(data):
    """
    Remove PKCS7 padding from decrypted data

    The encryption tool adds PKCS7 padding (main.cpp lines 112-116):
    - Calculates padding needed to reach block size (16 bytes)
    - Fills padding bytes with the padding length value

    Args:
        data: Padded plaintext data

    Returns:
        Unpadded data

    Raises:
        ValueError: If padding is invalid
    """
    if len(data) == 0:
        return data

    # Last byte contains the padding length
    padding_length = data[-1]

    # Validate padding length
    if padding_length > 16 or padding_length == 0:
        raise ValueError(f"Invalid padding length: {padding_length}")

    # Verify all padding bytes have the correct value
    for i in range(padding_length):
        if data[-(i+1)] != padding_length:
            raise ValueError(f"Invalid padding at position {-(i+1)}")

    # Remove padding
    return data[:-padding_length]

def decrypt_file(input_filename, output_filename):
    """
    Decrypt a file encrypted by winrev_lvl3.exe

    Decryption process (reverse of main.cpp encrypt_file_aes256):
    1. Read encrypted file
    2. Initialize AES-256-CBC cipher with key and IV
    3. Decrypt the data
    4. Remove PKCS7 padding
    5. Write decrypted data to output file

    Args:
        input_filename: Path to encrypted .enc file
        output_filename: Path where decrypted file will be saved

    Returns:
        True if successful, False otherwise
    """
    print(f"[*] Reading encrypted file: {input_filename}")

    # Read the encrypted file
    try:
        with open(input_filename, 'rb') as f:
            ciphertext = f.read()
    except FileNotFoundError:
        print(f"[ERROR] File not found: {input_filename}")
        return False
    except Exception as e:
        print(f"[ERROR] Failed to read file: {e}")
        return False

    if len(ciphertext) == 0:
        print("[ERROR] Encrypted file is empty")
        return False

    print(f"[*] Encrypted data size: {len(ciphertext)} bytes")

    # Validate that ciphertext length is multiple of block size (16 bytes)
    if len(ciphertext) % 16 != 0:
        print(f"[ERROR] Invalid ciphertext length: {len(ciphertext)} (must be multiple of 16)")
        return False

    # Create AES-256-CBC cipher (matching main.cpp lines 45-58)
    print("[*] Initializing AES-256-CBC cipher...")
    cipher = Cipher(
        algorithms.AES(AES_KEY),  # 32-byte key for AES-256
        modes.CBC(IV),             # CBC mode with zero IV
        backend=default_backend()
    )

    # Decrypt the data (reverse of main.cpp lines 139-148)
    print("[*] Decrypting...")
    decryptor = cipher.decryptor()
    try:
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    except Exception as e:
        print(f"[ERROR] Decryption failed: {e}")
        return False

    print(f"[*] Decrypted data size (with padding): {len(padded_plaintext)} bytes")

    # Remove PKCS7 padding (reverse of main.cpp lines 112-116)
    print("[*] Removing PKCS7 padding...")
    try:
        plaintext = remove_pkcs7_padding(padded_plaintext)
    except ValueError as e:
        print(f"[ERROR] Failed to remove padding: {e}")
        print("[!] This might indicate wrong key or corrupted data")
        return False

    print(f"[*] Final decrypted data size: {len(plaintext)} bytes")

    # Write decrypted data to output file (reverse of main.cpp lines 150-161)
    print(f"[*] Writing decrypted file: {output_filename}")
    try:
        with open(output_filename, 'wb') as f:
            f.write(plaintext)
    except Exception as e:
        print(f"[ERROR] Failed to write output file: {e}")
        return False

    return True

def main():
    """Main entry point"""
    print("=" * 60)
    print("  AES-256 Decryption Tool for winrev_lvl3.exe")
    print("=" * 60)
    print()

    # Check command line arguments
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <encrypted_file.enc>")
        print()
        print("Description:")
        print("  Decrypts files encrypted by winrev_lvl3.exe")
        print()
        print("Example:")
        print(f"  python {sys.argv[0]} document.txt.enc")
        print("  Output: document.txt")
        sys.exit(1)

    input_file = sys.argv[1]

    # Validate input file exists
    if not os.path.exists(input_file):
        print(f"[ERROR] File does not exist: {input_file}")
        sys.exit(1)

    # Generate output filename by removing .enc extension
    if input_file.lower().endswith('.enc'):
        output_file = input_file[:-4]  # Remove .enc
    else:
        output_file = input_file + '.decrypted'
        print(f"[!] Warning: Input file doesn't have .enc extension")

    print(f"Input file:  {input_file}")
    print(f"Output file: {output_file}")
    print()

    # Check if output file already exists
    if os.path.exists(output_file):
        response = input(f"[!] Output file '{output_file}' already exists. Overwrite? (y/n): ")
        if response.lower() not in ['y', 'yes']:
            print("[*] Aborted by user")
            sys.exit(0)

    # Decrypt the file
    print("[*] Starting decryption process...")
    print()

    if decrypt_file(input_file, output_file):
        print()
        print("=" * 60)
        print("[SUCCESS] File decrypted successfully!")
        print("=" * 60)

        # Display file information
        input_size = os.path.getsize(input_file)
        output_size = os.path.getsize(output_file)

        print(f"\nFile Information:")
        print(f"  Encrypted file:  {input_file} ({input_size} bytes)")
        print(f"  Decrypted file:  {output_file} ({output_size} bytes)")
        print(f"  Padding removed: {input_size - output_size} bytes")

        sys.exit(0)
    else:
        print()
        print("=" * 60)
        print("[FAILED] Decryption failed!")
        print("=" * 60)
        sys.exit(1)

if __name__ == "__main__":
    main()
