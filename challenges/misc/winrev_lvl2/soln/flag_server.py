#!/usr/bin/env python3
"""
CTF Flag Server - Level 2
This script emulates a network server that communicates with the
Windows reverse engineering challenge binary to extract the flag.

The server:
1. Listens on localhost (127.0.0.1) TCP port 61187
2. Accepts incoming connections from the challenge binary
3. Sends the magic phrase "give me the flag please?" to trigger flag reveal
4. Receives and displays the flag from the binary

Usage:
    python flag_server.py

Then run the compiled winrev_lvl2.exe in another terminal.
"""

import socket
import sys

# Server configuration
HOST = '127.0.0.1'  # Localhost
PORT = 61187         # Port the challenge binary expects

# The magic phrase that triggers the flag reveal
MAGIC_PHRASE = "give me the flag please?"


def start_server():
    """Start the TCP server and wait for the challenge binary to connect."""

    print("[*] CTF Flag Server - Level 2")
    print("[*] ========================================")
    print(f"[*] Starting server on {HOST}:{PORT}")

    # Create TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Set socket options to allow reuse of address
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        # Bind to the address and port
        server_socket.bind((HOST, PORT))

        # Listen for incoming connections (max 1 queued connection)
        server_socket.listen(1)

        print(f"[+] Server is listening on {HOST}:{PORT}")
        print("[*] Waiting for challenge binary to connect...")
        print("[*] (Run winrev_lvl2.exe now)")
        print()

        # Accept incoming connection
        client_socket, client_address = server_socket.accept()

        print(f"[+] Connection received from {client_address[0]}:{client_address[1]}")
        print(f"[*] Sending magic phrase: '{MAGIC_PHRASE}'")

        # Send the magic phrase to trigger flag reveal
        client_socket.sendall(MAGIC_PHRASE.encode('utf-8'))

        print("[*] Magic phrase sent successfully!")
        print("[*] Waiting for flag response from binary...")
        print()

        # Receive the flag from the binary
        flag_data = client_socket.recv(1024)

        if flag_data:
            flag = flag_data.decode('utf-8').strip()
            print("[+] ========================================")
            print("[+] FLAG CAPTURED!")
            print("[+] ========================================")
            print(f"[+] {flag}")
            print("[+] ========================================")
            print()
        else:
            print("[-] No data received from binary")

        # Close the client connection
        client_socket.close()

    except socket.error as e:
        print(f"[-] Socket error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n[*] Server interrupted by user")
    except Exception as e:
        print(f"[-] Error: {e}")
    finally:
        # Close the server socket
        server_socket.close()
        print("[*] Server shut down")


if __name__ == "__main__":
    start_server()
