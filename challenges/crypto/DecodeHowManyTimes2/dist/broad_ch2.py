import base64

def decode_base64(input_string):
    # there is literally nothing
    pass

if __name__ == "__main__":
    encoded_flag = ''
    with open('decode_me.txt', 'r') as file:
        encoded_flag = file.readlines()

    # TODO: remember to finish the decoding thing
    # rmber that the flag starts with 'SIG{'
    decoded_flag = decode_base64(encoded_flag)

    print(decoded_flag) # I sure do hope the decoded flag isn't more encrypted.