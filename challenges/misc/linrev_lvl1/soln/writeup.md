# linrev_lvl1 - CTF Writeup

## Challenge Overview
This is a Linux reverse engineering challenge where we need to analyze a binary to extract the flag.

## Initial Analysis

Running the binary without any arguments produces the following output:

```bash
[baesenseii@ops app]$ ./linrev_lvl1
what do you want?
```

This suggests the binary expects some specific input to reveal the flag.

## Reverse Engineering with Ghidra

Loading the binary into Ghidra's decompiler reveals the following C pseudocode for the `main` function:

```c
undefined8 main(int param_1,long param_2)

{
  int iVar1;
  int iVar2;
  int iVar3;
  undefined8 uVar4;
  size_t sVar5;
  long in_FS_OFFSET;
  bool bVar6;
  int local_4c;
  char local_38 [40];
  long local_10;

  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  iVar1 = v_check();
  if (iVar1 == 0) {
    uVar4 = 1;
  }
  else if (param_1 == 2) {
    sVar5 = strlen(*(char **)(param_2 + 8));
    iVar1 = (int)sVar5;
    sVar5 = strlen("givemetheflagezpz");
    iVar2 = (int)sVar5;
    bVar6 = iVar1 == iVar2;
    local_4c = 0;
    while( true ) {
      iVar3 = iVar1;
      if (iVar1 <= iVar2) {
        iVar3 = iVar2;
      }
      if (iVar3 <= local_4c) break;
      if (((local_4c < iVar1) && (local_4c < iVar2)) &&
         (*(char *)((long)local_4c + *(long *)(param_2 + 8)) != "givemetheflagezpz"[local_4c])) {
        bVar6 = false;
      }
      local_4c = local_4c + 1;
    }
    if ((bVar6) && (iVar1 == iVar2)) {
      proc(local_38);
      puts(local_38);
    }
    else {
      puts("what do you want?");
    }
    uVar4 = 0;
  }
  else {
    puts("what do you want?");
    uVar4 = 0;
  }
```

## Understanding the Code

### Function Signature Analysis
The main function signature can be mapped to the standard C definition:

```c
int main(int argc, char* argv[])
```

Where:
- `param_1` corresponds to `argc` (argument count)
- `param_2` corresponds to `argv` (argument vector)

### Key Observations

1. **Argument Count Check**: The code checks if `param_1 == 2`, meaning it expects exactly one command-line argument (plus the program name).

2. **Hardcoded String**: The decompiled code reveals a hardcoded string: `"givemetheflagezpz"`

3. **String Comparison**: The code at `*(char **)(param_2 + 8)` accesses `argv[1]` (the first user-provided argument). The `+8` offset is because `argv` is an array of pointers, and on 64-bit systems, each pointer is 8 bytes.

4. **Character-by-Character Comparison**: The while loop performs a manual string comparison between the user input and `"givemetheflagezpz"`.

5. **Success Condition**: If the strings match, the `proc()` function is called with `local_38` as an argument, which presumably generates and prints the flag.

## Getting the Flag

Based on the analysis, we need to provide the string `"givemetheflagezpz"` as a command-line argument:

```bash
[baesenseii@ops dist]$ ./linrev_lvl1 givemetheflagezpz
SPARK{R3V_15nT_50_b4d_14h!}
```

