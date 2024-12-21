import sys

def check():
    if len(sys.argv) > 1:
        return sys.argv[1]
    else:
        print("Example: python3 numbertoflag.py <number>")
        sys.exit(1)

def convert(number: str):
    try:
        num = int(number)
        byte_array = num.to_bytes((num.bit_length() + 7) // 8, byteorder='big')
        return byte_array.decode('ascii')
    except (ValueError, OverflowError):
        print("Input is invalid.")
        sys.exit(1)

if __name__ == "__main__":
    param = check()
    print(f"Decoded Value: {convert(param)}")