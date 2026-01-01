# hosehbo

"When the stack fails you, the exception handler becomes your playground." - Anonymous PWN Player, 2025

Welcome to a more advanced Windows exploitation challenge! This binary has Structured Exception Handling (SEH) in place, but that doesn't mean it's safe from exploitation. The classic SEH chain overflow technique awaits those who dare to dive deeper into Windows internals.

Can you corrupt the exception handler chain and hijack program execution? The flag lies beyond the exception boundary!

A local copy of the Windows service is included in this compressed 7z file. Reverse engineer it and attempt to exploit it locally first! Once you are able to do so, you can send your payload over to the following host (use netcat to test it):

``nc winpwns.sparkctf.org 35543``

## Summary
- **Author:** Sayed Hamzah (@BaeSenseii)
- **Category:** Pwn
- **Learning Objective:** Understanding SEH-based buffer overflow exploitation on Windows

## Files
- [`hosehbo.7z`](./dist/hosehbo.7z)

## Hints
- `Look for a pop pop ret gadget in the binary.` (200 points)
- `The SEH chain can be your stepping stone to execution control. What happens when you overflow past the buffer?` (200 points)

## Flags
- `SPARK{s3h_ch41n_0v3rfl0w_pwn3d!}`
