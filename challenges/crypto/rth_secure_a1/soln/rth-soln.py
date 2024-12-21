encrypted_message = ''
with open('../dist/encrypted.txt', 'r') as file:
    encrypted_message = [int(line.strip()) for line in file.readlines()]

n = 5723
d = 5021

# Decrypting the message
decrypted_message = []
for c in encrypted_message:
    m = pow(c, d, n)
    decrypted_message.append(m)

decrypted_message_str = ''.join(chr(m) for m in decrypted_message)
print(f"Decrypted message: {decrypted_message_str}")