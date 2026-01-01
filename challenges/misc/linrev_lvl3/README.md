# linrev_lvl3

"This is just outright insane. Take your time on this!" - The Binary's Only Message, 2025

You thought level 2 was tough? Well, buckle up! This time, the developer has gone absolutely wild with obfuscation. The flag is buried under multiple layers of transformations - nibble swapping, bit rotations, XOR with rotating keys, and NOT operations. But here's the twist: even if you reverse all that crypto, you won't see the flag... because the binary only reveals it over a network connection!

This binary expects to talk to a very specific server on a very specific port. Get the handshake wrong, and all you'll see is that cryptic error message. Get it right, and the binary will decode its treasure and send it straight to you over TCP. Time to combine your reverse engineering skills with some network analysis. Can you figure out what the binary wants to hear, and more importantly, what it has to say?

## Summary
- **Author:** Sayed Hamzah (@BaeSenseii)
- **Category:** Misc
- **Learning Objective:** Advanced reverse engineering with network protocol analysis, multi-layer deobfuscation, and dynamic analysis techniques

## Requirements
- linrev_lvl2

## Files
- [`linrev_lvl3.7z`](./dist/linrev_lvl3.7z)

## Hints
- `The binary wants to talk to someone on localhost. What port is it looking for?` (200 points)
- `There's a specific handshake protocol. The binary expects certain messages and sends specific responses. Trace the network functions!` (200 points)
- `You don't need to reverse the entire decryption algorithm - just set up the right server and let the binary do the work for you!` (200 points)

## Flags
- `SPARK{w04h_y0uR3_g3tt1ng_th3_h4nG_0f_R3V}`
