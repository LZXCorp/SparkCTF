#!/usr/bin/env python3
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python decrypt.py <encrypted_file>")
        sys.exit(1)

    filename = sys.argv[1]

    # Read the encrypted data
    with open(filename, 'rb') as f:
        encrypted_data = f.read()

    if len(encrypted_data) == 0:
        print("Error: File is empty")
        sys.exit(1)

    # Get the first byte of the key by XORing first byte of encrypted data with 'S'
    first_byte = encrypted_data[0] ^ ord('S')
    print(f"First key byte: 0x{first_byte:02x} ({first_byte})")

    # Reconstruct the full key by incrementing each byte
    key_length = len(encrypted_data)
    key = bytearray()

    for i in range(key_length):
        new_byte_key = (first_byte + i) % 256
        key.append(new_byte_key)  # Wrap around at 256

    print(f"Key length: {key_length}")
    print(f"Key (first 16 bytes): {key[:16].hex()}")

    # Decrypt the data by XORing with the key
    decrypted_data = bytearray()
    for i in range(len(encrypted_data)):
        decrypted_data.append(encrypted_data[i] ^ key[i])

    # Print the decrypted data
    print("\nDecrypted data:")
    print(decrypted_data.decode('utf-8', errors='replace'))

    # Optionally save to file
    output_file = filename + '.decrypted'
    with open(output_file, 'wb') as f:
        f.write(decrypted_data)
    print(f"\nDecrypted data saved to: {output_file}")

if __name__ == "__main__":
    main()
