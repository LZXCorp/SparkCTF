import pickle
import socket
import ast
import time
import threading

# Initialize the user database
user1 = {'Status': 'Running', 'User': 'Jack'}
user2 = {'Status': 'Red', 'User': 'Her', 'Access': 'ERROR', 'Item': 'Ring'}
user3 = {'Status': 'Stopped', 'User': 'Tom', 'Access': False, 'Level': False}
user4 = {'Status': 'Green'}
user5 = {'Status': 'Enabled', 'User': 'Tom', 'Level': '3000'}
user6 = {'Status': 'Unknown', 'User': 'ERROR', 'Access': 'ERROR', 'Level': 'ERROR'}

db = {
    'User1': user1,
    'User2': user2,
    'User3': user3,
    'User4': user4,
    'User5': user5,
    'User6': user6
}

# Serialize the database (could be used for testing)
x = pickle.dumps(db)


# Start the TCP server
HOST = '0.0.0.0'
PORT = 24681

def handle_client(conn, addr):
    print(f"Connection from {addr}")
    conn.sendall(b'Loading Configuration.\n')
    time.sleep(0.7)
    conn.sendall(b'Loading Configuration..\n')
    time.sleep(0.7)
    conn.sendall(b'Loading Configuration...\n')
    time.sleep(0.7)
    conn.sendall(b'---- API LISTENING ----\n')
    conn.sendall(x)
    conn.sendall(b'\n')
    conn.sendall(b'POST REQUEST:')
    try:
        while True:
            data = conn.recv(4096)
            if not data:
                conn.sendall(b"No data received.\n")
                break  # Disconnect

            try:
                # Safe evaluation, then deserialization
                eval_expr = ast.literal_eval(data.decode())
                user_serial = pickle.loads(eval_expr)

                # Check condition
                if (user_serial.get('User3', {}).get('Access')) == True:
                    conn.sendall(b"DATABASE UPDATE SUCCESSFUL\n")
                    conn.sendall(b"SPARK25{PICKLE_1n53cur3_d353r14l1z4710n}\n")
                    break  # Success: end connection


            except Exception:
                conn.sendall(b"INVALID INPUT\nPOST REQUEST:\n")
                continue  
    except Exception as e:
        print(f"Error with {addr}: {e}")
    finally:
        conn.close()
        print(f"Connection with {addr} closed.")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    s.settimeout(1.0)  # timeout for accept

    print(f"Server listening on {HOST}:{PORT}...")

    try:
        while True:
            try:
                conn, addr = s.accept()
                client_thread = threading.Thread(target=handle_client, args=(conn, addr))
                client_thread.start()
            except socket.timeout:
                continue
    except KeyboardInterrupt:
        print("\n[!] Server shutting down due to Ctrl+C.")
    except Exception as e:
        print(f"[!] Unexpected error: {e}")
    finally:
        s.close()
