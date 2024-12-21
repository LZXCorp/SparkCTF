import os
import sys
import hashlib

def fibonacci_sequence(n):
    """Generate a Fibonacci sequence of length n."""
    sequence = [0, 1]
    for _ in range(2, n):
        sequence.append(sequence[-1] + sequence[-2])
    return sequence[:n]

def decrypt_file(encrypted_file, output_file):
    """Decrypt the file using the Fibonacci sequence."""
    with open(encrypted_file, 'rb') as f:
        encrypted_data = bytearray(f.read())

    sequence = fibonacci_sequence(len(encrypted_data))
    decrypted_data = bytearray((byte - seq_val) % 256 for byte, seq_val in zip(encrypted_data, sequence))

    with open(output_file, 'wb') as f:
        f.write(decrypted_data)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python file_decryptfib.py <input_file> <output_file>")
        sys.exit(1)

    mode = sys.argv[1].lower()
    input_file = os.path.join(os.getcwd(), sys.argv[2])
    output_file = os.path.join(os.getcwd(), sys.argv[3])

    decrypt_file(input_file, output_file)
    print(f"File decrypted and saved to {output_file}")