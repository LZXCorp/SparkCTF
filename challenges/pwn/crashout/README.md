# crashout

"Sometimes, the best way to find a vulnerability is to just... crash it." - Anonymous PWN Player, 2025

Welcome to your first Windows binary exploitation challenge! You've been given an executable that reads user input, however something about the way it handles that input seems a little... fragile. Can you figure out what happens when you give it more than it can handle?

A local copy of the Windows service is included in this compressed 7z file. Reverse engineer it and attempt to exploit it locally first! Once you are able to do so, you can send your payload over to the following host (use netcat to test it):

``nc winpwns.sparkctf.org 35541``

## Summary
- **Author:** Sayed Hamzah (@BaeSenseii)
- **Category:** Pwn
- **Learning Objective:** Introduction to basic buffer overflow vulnerabilities in Windows binaries

## Files
- [`crashout.7z`](./dist/crashout.7z)

## Hints
- `The binary reads from a file. What happens when the file content exceeds the buffer size?` (200 points)
- `64 bytes might just be the magic number here.` (200 points)

## Flags
- `SPARK{buff3r_0v3rfl0w_v1ct0ry!}`
