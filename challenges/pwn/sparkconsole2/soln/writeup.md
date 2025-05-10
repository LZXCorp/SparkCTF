# Solution

## Analysis

1. The program notably has PIE enabled, so we need to find a way to leak out the function addresses.
   ```bash
    # checksec sparkconsole 
    [*]
        Arch:       i386-32-little
        RELRO:      Full RELRO
        Stack:      No canary found
        NX:         NX enabled
        PIE:        PIE enabled
        Stripped:   No
    ```

    If you want the assembly code, type in this command:
    ```bash
    objdump -d -M intel --source sparkconsole > objdump.txt
    ```

2. The program code contains a hidden command `echo`.
   ```c
    if (sscanf(cmd, "echo %s", arg) == 1) {
        if (strstr(arg, "%n") != NULL) {
            printf("Error: Error Occured while parsing string\n");
        } else {
            printf(arg);
            printf("\n");
        }
        continue;
    }
    ```

3. When looking closely, the `echo` command is vulnerable to format string leaks. \
   \
   We can make use of this to leak out addresses. In x86 programs specifically, we can leak out the stack values such as the `ret` value (back to `main()`).

4. As for the actual sizes of the buffers, there are two buffers
   
   The start of `buffer1` is at `0x2e`
   ```asm
   1593:	8d 45 d2             	lea    eax,[ebp-0x2e]
   ```

   The start of `buffer2` is at `0xe`.
   ```asm
   1571:	c7 45 f2 78 78 78 78 	mov    DWORD PTR [ebp-0xe],0x78787878
   ```

   From this, we can deduce the size of `buffer1` as `0x2e - 0xe = 32`.

   As for `buffer2`, we need to find the end, which is,
   ```asm
   1578:	66 c7 45 f6 78 78    	mov    WORD PTR [ebp-0xa],0x7878
   ```

   `DWORD` indicates 4 bytes while `WORD` indicated 2 bytes. Thus, `buffer2` size is `4 + 2 = 6`.

   Thus, the calculated offset is **38**.

5. When the program reaches to the end of `main()`, it has to go through multiple `pop` operations.
   ```asm
        ...
        1608:	59                   	pop    ecx
        1609:	5b                   	pop    ebx
        160a:	5d                   	pop    ebp
        160b:	8d 61 fc             	lea    esp,[ecx-0x4]
        160e:	c3                   	ret
   ```

   However, `main()` does a `ret` with original `esp`, so it is not possible to overwrite the `ret` address.

   Good news is, we can control the value to pop into the `ecx` register, which is used to set the `esp` register with it to perform stack pivoting.

6. The `read_flag_file`'s offset is at `0x1278`.
   ```asm
   00001278 <read_flag_file>:
   ```

## Leaking Addresses

1. We can leak addresses using format string vulnerability in `echo`.
   ```bash
   $ echo %p
   0x5655a0e3
   ```

2. The script [`find_seq.py`](./find_seq.py) is created to find the exact addresses we want. For this writeup, we want the stack address at `ebp` and the address of `main()`.
   \
   From the `main()` address, we can find the address of `read_flag_file()` using [simple offset calculations](https://ir0nstone.gitbook.io/notes/binexp/stack/pie/pie-exploit).
   \


> [!note]
> Do note that the `main()` address leaked is **not** the actual address, and it is just the `ret` address back to some portion of `main()`.

## Payload Creation

The payload should follow this structure:

- 32 `b'A'`'s
- `ebp-4` (for `ecx`)
- `0xdeadbeef` (for `ebx` since it will not be used)
- `read_flag_file()` address (for `ebp`)

## Exploiting

Have a look at the [`soln.py`](./soln.py) to see the full script and how it was created.