import socket

def caesar_decrypt(ciphertext: str, shift: int) -> str:
    """Decrypt Caesar cipher text with a given shift"""
    result = []
    for ch in ciphertext:
        if 'a' <= ch <= 'z':
            offset = ord('a')
            shifted = chr(((ord(ch) - offset - shift) % 26) + offset)
            result.append(shifted)
        else:
            result.append(ch)
    return "".join(result)

def main():
    host = input("Enter server IP: ").strip()
    port = int(input("Enter server port: ").strip())

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))

        # Receive the Caesar cipher text
        data = s.recv(4096).decode(errors="ignore").strip()
        print(f"[Server] {data}")

        # Try all possible Caesar shifts
        for shift in range(1, 26):
            attempt = caesar_decrypt(data, shift)
            print(f"[*] Trying shift {shift}: {attempt}")

            # Send attempt to server
            s.sendall((attempt + "\n").encode())

            # Receive response
            response = s.recv(4096).decode(errors="ignore")
            print(f"[Server Response] {response.strip()}")

            if not "Wrong" in response and not "Error" in response and not "Bye" in response:
                print(f"[+] Found correct shift: {shift}")
                break
            elif "Error" in response or "Bye" in response:
                break

if __name__ == "__main__":
    main()