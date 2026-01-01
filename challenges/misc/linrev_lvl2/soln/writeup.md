# linrev_lvl2 - CTF Writeup

## Challenge Overview
This is a Linux reverse engineering challenge where we're presented with a binary that requires specific command-line arguments to reveal the flag. The challenge title hints at this being a "levelled up" version of a previous challenge.

## Initial Reconnaissance

Running the binary without arguments gives us a simple output:

```bash
[baesenseii@ops dist]$ ./linrev_lvl2
It's me again, but i've levelled up
```

No flag here, so we need to dig deeper. Time to fire up a decompiler.

## Static Analysis

### Main Function

Decompiling the binary reveals the following main function:

```c
undefined8 main(int param_1,long param_2)

{
  int iVar1;
  undefined8 uVar2;
  long in_FS_OFFSET;
  char local_38 [40];
  long local_10;

  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  iVar1 = 0;
  do {
    iVar1 = iVar1 + 1;
  } while (iVar1 != 100);
  if (param_1 == 3) {
    iVar1 = v1(*(undefined8 *)(param_2 + 8),*(undefined8 *)(param_2 + 0x10));
    if (iVar1 == 0) {
      puts("It\'s me again, but i\'ve levelled up");
      uVar2 = 0;
    }
    else {
      r1();
      puts(local_38);
      uVar2 = 0;
    }
  }
  else {
    puts("It\'s me again, but i\'ve levelled up");
    uVar2 = 1;
  }
  if (local_10 == *(long *)(in_FS_OFFSET + 0x28)) {
    return uVar2;
  }
```

### Understanding the Main Function

The decompiled main function signature can be mapped to the standard C definition:

```c
int main(int argc, char* argv[])
```

Where:
- `param_1` corresponds to `argc` (argument count)
- `param_2` corresponds to `argv` (argument vector, pointer to array of strings)

The key observation here is the condition `if (param_1 == 3)` - this means the program expects exactly 3 arguments (program name + 2 additional arguments). When this condition is met, the program calls a validation function `v1()` with two arguments extracted from `argv[1]` and `argv[2]`.

### The Validation Function (v1)

The critical validation logic is contained in the `v1` function:

```c
bool v1(long param_1,long param_2)

{
  long lVar1;
  long lVar2;

  if ((param_1 != 0) && (param_2 != 0)) {
    lVar1 = __isoc23_strtoull(param_1,0,0x10);
    lVar2 = __isoc23_strtoull(param_2,0,0x10);
    return lVar2 == 0xdeadbeef && lVar1 == 0xdeadbeef;
  }
  return false;
}
```

### Key Findings

The `v1` function performs the following checks:

1. Ensures both parameters are non-null
2. Uses `__isoc23_strtoull()` to convert the string arguments to unsigned long long integers
3. The third parameter `0x10` indicates hexadecimal base conversion
4. Returns `true` only if both values equal `0xdeadbeef`

The logic shows that if `v1()` returns `true` (non-zero), the program executes `r1()` which presumably decrypts/reveals the flag.

## Solution

Based on the analysis, we need to provide two command-line arguments, both with the hexadecimal value `0xdeadbeef`. Let's test this:

```bash
[baesenseii@ops dist]$ ./linrev_lvl2 0xdeadbeef 0xdeadbeef
SPARK{0k4y_Th15_15_4_B11T_D1FF}
```

Success! The flag is revealed.