import socket
import re

def strip_ansi(text: str) -> str:
    """Remove ANSI escape codes"""
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)

def main():
    host = input("Enter server IP: ").strip()
    port = int(input("Enter server port: ").strip())

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))

        # Receive phrase
        data = s.recv(4096).decode(errors="ignore")
        print(f"[Server] {data.strip()}")

        # Strip ANSI codes
        stripped = strip_ansi(data).strip()
        print(f"[ANSI Stripped] {stripped}")

        # Send back the cleaned phrase
        s.sendall((stripped + "\n").encode())

        # Get server response
        response = s.recv(4096).decode(errors="ignore")
        print(f"[Server Response] {response.strip()}")

if __name__ == "__main__":
    main()