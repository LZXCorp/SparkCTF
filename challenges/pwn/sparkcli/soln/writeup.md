# Solution

## Functionality and Code Analysis

A shell-like interface with three commands available to use.

```bash
Spark Shell!
Available commands: ls, cat <file>, exit

$
```

There seems to be a PIN requirement as well.

```bash
$ cat pin.txt
046233$ exit

Before you leave, please enter the PIN: 046233
Incorrect PIN. Better luck next time!
```

The program code shows signs of a canary prevention, and buffer overflow prevention if we type in the wrong PIN.

```c
int sub_1A24()
{
  char s[78]; // [rsp+0h] [rbp-50h] BYREF
  __int16 s1; // [rsp+4Eh] [rbp-2h] BYREF

  puts("Spark Shell!");
  puts("Available commands: ls, cat <file>, exit\n");
  sub_16A6();
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

`checksec` also shows that the program has ASLR enabled, so we also need to do a bit of calculating.

```bash
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        PIE enabled
    SHSTK:      Enabled
    IBT:        Enabled
```


## PIE and Canary

To solve the PIE issue, we can make use of a hidden command, `log`, that prints the address of `sub_14B2` + `v0`.

```bash
$ log
Logged Signature: 0x555555554000
```

```c
int sub_165C()
{
  ...
  v0 = atoi(nptr);
  return printf("Logged Signature: %p\n", (char *)sub_165C + v0);
}

int sub_16A6()
{
  ...
      if ( strcmp(s, "log") )
        break;
      sub_165C();
  ...
}
```

And in this case, `v0` is the PIN number.

```c
ptr = sub_1469("pin.txt");
...
strncpy(nptr, ptr, 6u);
```

To calculate the base address, we will need to make use of the equation below:

```
*sub_14b2() = Logged Signature - PIN
Base Address = *sub_14b2() - 0x165c
```

As for the canary, all we need to do is to get the saved contents of `canary.txt`.

```bash
$ cat canary.txt
N$ exit
```

Sometimes it doesn't show up, so instead we may need to do some stuff like using [`find_canary.py`](./find_canary.py) to find the canary bytes.

```bash
Found canary bytes: 0x02 0x4e

Leaked Canary: N\x02
```

## Buffer Overflow

Now to create a payload that satisfies the following conditions:

1. The first 6 bytes of the payload should be the PIN number,
2. From 78-80 of the payload should be `\x4e\x02`,
3. The rest of the payload should be a cyclic payload (to find offset).

After that is done, you can make use of a ROP chain to perform a ret2syscall to get bash or read the contents of the flag.txt file.