import binascii

characters = "abcdefghijklmnopqrstuvwxyz_}{1234567890"
def encrypt(flag, key):
    encrypt1 = ""
    for ch in flag:
        if ch in characters:
            index = characters.index(ch)
            sh = (index + key) % len(characters)
            encrypt1 += characters[sh]
        else:
            encrypt1 += ch
    return encrypt1


flag = input("Enter a message to encrypt (flag): ").lower()
key = int(input(f"Input a key as a number between 1 and {len(characters)-1}: "))
while not (key>=1 and key<=len(characters)-1):
  print("Invalid key, try again!")
  key = int(input(f"Input a key as a number between 1 and {len(characters)-1}: "))
  #guess the key


encrypt1 = encrypt(flag, key) 
encrypt2 = encrypt1.encode()
encrypt3 = binascii.hexlify(encrypt2)
encrypt4 = bin(int(encrypt3, 16))[2:]
print(encrypt4)
