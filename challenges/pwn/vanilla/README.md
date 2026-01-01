# vanilla

"Return to where it all began... the flag function awaits." - Anonymous PWN Player, 2025

A classic Windows binary exploitation challenge! There's a hidden function somewhere in the binary that will give you the flag - you just need to find a way to call it.

A local copy of the Windows service is included in this compressed 7z file. Reverse engineer it and attempt to exploit it locally first! Once you are able to do so, you can send your payload over to the following host (use netcat to test it):

``nc winpwns.sparkctf.org 35542``

## Summary
- **Author:** Sayed Hamzah (@BaeSenseii)
- **Category:** Pwn
- **Learning Objective:** Understanding ret2win buffer overflow exploitation and return address overwriting

## Files
- [`vanilla.7z`](./dist/vanilla.7z)

## Hints
- `Find the offset to the return address using a cyclic pattern.` (200 points)
- `There's a function called get_flag() hiding in the binary. What's its address?` (200 points)

## Flags
- `SPARK{s4m3_0lD_b0f_2_g3t_fl4g}`
