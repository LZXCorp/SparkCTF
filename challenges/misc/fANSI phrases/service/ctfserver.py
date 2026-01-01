import socket
import threading
import random
import re
import os

FLAG_FILE = "flag.txt"
TIMEOUT_SECS = 3.0

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

# Some ANSI colours
COLORS = ["\033[31m", "\033[32m", "\033[33m", "\033[34m", "\033[35m", "\033[36m"]
RESET = "\033[0m"

def colorize_text(text: str) -> str:
    """Randomly colorize a few characters in the text"""
    chars = list(text)
    num_to_color = random.randint(1, max(1, len(chars)//3))  # color up to one-third of total characters
    indices = random.sample(range(len(chars)), num_to_color)

    for i in indices:
        color = random.choice(COLORS)
        chars[i] = f"{color}{chars[i]}{RESET}"

    return "".join(chars)

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

    # Pick a random phrase
    phrase = randomise_text()
    colored_phrase = colorize_text(phrase)

    try:
	# Apply timeout
        conn.settimeout(TIMEOUT_SECS)

	# Send to client
        conn.sendall((colored_phrase + "\n").encode())

        # Receive and sanitize input
        data = conn.recv(1024).decode(errors="ignore")
        data = sanitize_input(data).strip()        
	
	# Compare input
        if data == phrase:
            conn.sendall(f"\nCorrect! Flag: {FLAG}\n".encode())
        else:
            conn.sendall(b"\nWrong answer. Bye!\n")
    except socket.timeout:
        conn.sendall(b"\nToo slow. Bye!\n")
    except Exception:
        conn.sendall(b"\nError processing your input. Bye!\n")
    finally:
        conn.close()
    print(f"[-] Connection closed {addr}")

def start_server(host="0.0.0.0", port=4444):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(50)
    print(f"[*] Server listening on {host}:{port}")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    start_server()
