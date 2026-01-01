#!/usr/bin/env python3
import socket
import os

HOST = '0.0.0.0'
PORT = 8551
FLAG_FILE = 'flag.txt'
CORRECT_VALUE = '63127519'

def handle_client(conn, addr):
    """Handle a single client connection"""
    print(f"[+] Connection from {addr}")

    try:
        # Send the challenge message
        message = (
            "I do not know what this text means at all, can you help me? "
            "It's supposed to tell me a 8 digit number, but i tried everything "
            "(including AI). The text is: fjw gmktt lrt gyl ftptr ojpt lrt rjrt\n\n"
            "Enter the 8 digit number: "
        )
        conn.sendall(message.encode())

        # Receive user input
        data = conn.recv(1024).decode().strip()
        print(f"[*] Received from {addr}: {data}")

        # Check if the input matches the correct value
        if data == CORRECT_VALUE:
            # Read and send the flag
            if os.path.exists(FLAG_FILE):
                with open(FLAG_FILE, 'r') as f:
                    flag = f.read().strip()
                response = f"\n[+] Correct! Here's your flag: {flag}\n"
            else:
                response = "\n[!] Correct answer, but flag file not found!\n"
        else:
            response = "\n[-] Incorrect! Try again.\n"

        conn.sendall(response.encode())

    except Exception as e:
        print(f"[!] Error handling client {addr}: {e}")
    finally:
        conn.close()
        print(f"[-] Connection closed: {addr}")

def main():
    """Main server loop"""
    # Create socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        # Bind and listen
        server.bind((HOST, PORT))
        server.listen(5)
        print(f"[*] Server listening on {HOST}:{PORT}")
        print(f"[*] Waiting for connections...")

        while True:
            # Accept connections
            conn, addr = server.accept()
            handle_client(conn, addr)

    except KeyboardInterrupt:
        print("\n[!] Server shutting down...")
    except Exception as e:
        print(f"[!] Server error: {e}")
    finally:
        server.close()

if __name__ == "__main__":
    main()
