import base64

def decode_base64(input_string):
    decoded_bytes = base64.b64decode(input_string)
    decoded_string = decoded_bytes.decode('utf-8')
    return decoded_string

if __name__ == "__main__":
    encoded_flag = ''
    with open('decode_me.txt', 'r') as file:
        encoded_flag = file.readlines()

    decoded_flag: str = encoded_flag[0].strip()
    for i in range(70):
        decoded_flag = decode_base64(decoded_flag)
        if decoded_flag.startswith('SIG{'):
            print(i+1)
            break
    print(decoded_flag)