import socket
import threading
import random
import re
import time

FLAG_FILE = "flag.txt"
TIMEOUT_SECS = 10

# Load flag from file
def get_flag():
    try:
        with open(FLAG_FILE, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"[!] Flag file '{FLAG_FILE}' not found!")
        return "FLAG_NOT_FOUND"

FLAG = get_flag()

# Randomised text generator
CHARACTERS = "abcdefghijklmnopqrstuvwxyz _"

def randomise_text():
    phrase = ""
    for x in range(random.randint(18,24)):
        phrase += CHARACTERS[random.randint(0, len(CHARACTERS)-1)]
    if phrase[:-1] == " ":
        return phrase[0:-1]
    else:
        return phrase

# Caesar cipher generator
def caesar_encrypt(text: str, shift: int) -> str:
    result_chars = []
    for ch in text:
        if 'a' <= ch <= 'z':
            offset = ord('a')
            shifted = chr(((ord(ch) - offset + shift) % 26) + offset)
            result_chars.append(shifted)
        else:
            result_chars.append(ch)
    return "".join(result_chars)

def sanitize_input(user_input: str) -> str:
    """
    Basic input sanitation:
    - Remove null bytes and control characters
    - Enforce max length
    """
    # Remove dangeours control characters (ASCII < 32 except \n, plus DEL 127)
    cleaned = re.sub(r"[\x00-\x09\x0B-\x1F\x7F]", "", user_input)

    # Enforce max length
    return cleaned[:200]

def handle_client(conn, addr):
    """Handles client connections"""
    print(f"[+] Connection from {addr}")

    # Randomly shift
    phrase = randomise_text()
    shift = random.randint(1, 25)  
    ciphertext = caesar_encrypt(phrase, shift)

    try:
	# Set timeout
        deadline = time.time() + TIMEOUT_SECS

	# Send to client
        conn.sendall((ciphertext + "\n").encode())

    # Loop accepting multiple guesses until deadline or success
        while True:
            remaining = deadline - time.time()
            if remaining <= 0:
                # Time's up
                try:
                    conn.sendall(b"\nToo slow. Bye!\n")
                except Exception:
                    pass
                break

            conn.settimeout(remaining)

            try:
                data = conn.recv(1024)
            except socket.timeout:
                try:
                    conn.sendall(b"\nToo slow. Bye!\n")
                except Exception:
                    pass
                break
            except Exception:
                break

            if not data:
                # client closed connection
                break

            # Decode and sanitize
            user_input = data.decode(errors="ignore")
            user_input = sanitize_input(user_input).strip()

            # Compare input
            if user_input == phrase:
                try:
                    conn.sendall(f"\nCorrect! Flag: {FLAG}\nKey: CSCiphered\n".encode())
                except Exception:
                    pass
                break
            else:
                try:
                    conn.sendall(b"\nWrong answer. Try again.\n")
                except Exception:
                    break

    except Exception as e:
        try:
            conn.sendall(b"\nError processing your input. Bye!\n")
        except Exception:
            pass
    finally:
        try:
            conn.shutdown(socket.SHUT_WR)
        except Exception:
            pass
        conn.close()
        print(f"[-] Connection closed {addr}")

def start_server(host="0.0.0.0", port=5555):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(50)
    print(f"[*] Server listening on {host}:{port}")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    start_server()
