# winrev_lvl3

"Cryptography in reverse engineering? Now that's what I call a challenge!" - Anonymous Security Researcher, 2025

Welcome to the advanced level of Windows reverse engineering! This challenge combines binary analysis with cryptographic concepts. You're provided with a Windows binary that implements file encryption using industry-standard cryptographic APIs, along with an encrypted file containing the flag.

Your mission is to reverse engineer the encryption process, extract the cryptographic parameters (key, IV, algorithm), and decrypt the provided file to reveal the hidden flag. This challenge will test your understanding of Windows Cryptography API Next Generation (CNG) and your ability to translate binary code into working decryption logic.

Are you ready to break some crypto? Fire up your disassembler and prepare to dive deep into cryptographic implementations!

Note: This binary was compiled for Windows x86_64. You'll need strong reverse engineering skills and familiarity with cryptographic concepts. Tools like Ghidra, IDA Pro, and Python (with cryptography libraries) will be essential.

## Summary
- **Author:** Sayed Hamzah (@BaeSenseii)
- **Category:** Misc
- **Learning Objective:** Advanced Windows reverse engineering with focus on cryptographic API analysis and implementation reversal

## Requirements
- winrev_lvl1

## Files
- [`winrev_lvl3.7z`](./dist/winrev_lvl3.7z)

## Hints
- `The binary uses Windows CNG API for encryption. Look for BCrypt* function calls!` (200 points)
- `The encryption key is obfuscated in the binary. Check for XOR operations with constant values!` (200 points)
- `AES requires a key and an IV. Find both in the decompiled code to decrypt the file!` (200 points)

## Flags
- `SPARK{@dv@nc3d_3ncryp710n_r3v3r53r}`
