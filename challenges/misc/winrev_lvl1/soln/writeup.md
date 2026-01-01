# winrev_lvl1 - CTF Writeup

## Challenge Overview
This is a Windows reverse engineering challenge where we need to analyze a binary executable to extract the flag.

## Initial Analysis

Running the binary without any special conditions will show its default behavior. However, the binary expects something specific before it reveals the flag.

## Reverse Engineering with Ghidra

Loading the binary into Ghidra (or your preferred disassembler such as IDA, Binary Ninja, or x64dbg) reveals interesting behavior in the program's logic.

### Key Findings

Upon decompiling the binary, we can observe that the program performs a file check operation. Specifically, the binary looks for a file with a very specific name in the same directory as the executable.

### File Name Discovery

Through static analysis, we can identify that the binary searches for a file named:

```
hellomynameis.special
```

The program uses Windows API functions to check for the existence of this file. When the file is present, the binary proceeds to reveal the flag.

## Getting the Flag

Based on our analysis, we need to create an empty file with the exact name the binary expects:

**Step 1:** Create the required file in the same directory as the executable:

```bash
# On Windows Command Prompt
type nul > hellomynameis.special

# On Windows PowerShell
New-Item -Path "hellomynameis.special" -ItemType File

# On Linux (using Wine or similar)
touch hellomynameis.special
```

**Step 2:** Run the binary:

```bash
winrev_lvl1.exe
```

**Step 3:** The binary will detect the file and print the flag:

```
SPARK{w1nd0w5_r3v3r53_3ng1n33r1ng_b451c5}
```

## Learning Points

This challenge demonstrates:
1. **Basic Static Analysis:** Understanding how to use disassemblers to analyze Windows binaries
2. **File System Interaction:** Recognizing how programs check for file existence using Windows APIs
3. **String Analysis:** Finding hardcoded strings within binaries that reveal program behavior
4. **Environmental Dependencies:** Understanding that some programs rely on specific files or conditions to execute properly

## Tools Used
- Ghidra / IDA Pro / Binary Ninja / x64dbg (for static analysis)
- Windows environment (for running the executable)

## Flag
`SPARK{w1nd0w5_r3v3r53_3ng1n33r1ng_b451c5}`
