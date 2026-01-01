# winrev_lvl2

"Network calls in a reverse engineering challenge? Now we're talking!" - Anonymous CTF Player, 2025

Ready to level up your Windows reverse engineering skills? This challenge introduces network communication analysis. A Windows binary has been programmed to communicate with a remote server before revealing its secrets.

Your mission is to understand the network protocol, figure out what the binary expects from the server, and extract the hidden flag. This challenge combines static analysis with understanding of network communications and Windows API calls.

Fire up your disassembler and maybe a network monitoring tool. The binary is waiting for a very specific conversation before it reveals the flag.

Note: This binary was compiled for Windows x86_64. You'll need a Windows environment or a compatible VM to run it. Tools like Ghidra, IDA, Wireshark, and x64dbg will be helpful for this challenge.

## Summary
- **Author:** Sayed Hamzah (@BaeSenseii)
- **Category:** Misc
- **Learning Objective:** Introduction to network-based reverse engineering and Windows socket API analysis

## Requirements
- winrev_lvl1

## Files
- [`winrev_lvl2.7z`](./dist/winrev_lvl2.7z)

## Hints
- `The binary is trying to connect somewhere. What port is it looking for?` (200 points)
- `Once connected, the server needs to send a specific message. Look for string comparisons in the decompiled code!` (200 points)

## Flags
- `SPARK{tcp_r3v3rs3_3ng1n33r_2025!}`
