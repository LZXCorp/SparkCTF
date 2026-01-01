#!/usr/bin/env python3
import socket

def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('127.0.0.1', 56441))
    server.listen(1)

    print("Test server listening on port 56441...")

    conn, addr = server.accept()
    print(f"Connection from {addr}")

    # Step 1: Send "hello linrev3"
    conn.send(b"hello linrev3")
    print("Sent: hello linrev3")

    # Step 2: Receive "sendflagoverthenet?"
    data = conn.recv(1024).decode()
    print(f"Received: {data}")

    if data == "sendflagoverthenet?":
        # Step 3: Send "yes"
        conn.send(b"yes")
        print("Sent: yes")

        # Step 4: Receive the flag
        flag = conn.recv(1024).decode()
        print(f"\n=== FLAG RECEIVED ===")
        print(f"Flag: {flag}")
        print(f"====================\n")

    conn.close()
    server.close()

if __name__ == "__main__":
    run_server()
