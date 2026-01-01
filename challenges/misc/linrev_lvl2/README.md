# linrev_lvl2

"I've leveled up my obfuscation game. Good luck finding the flag this time!" - Confident Developer, 2025

Remember that easy binary from level 1? Well, the developer wasn't too happy about how quickly you cracked it. They've come back with a vengeance, adding multiple layers of transformations, scattered data arrays, and some sneaky validation checks. This time, you'll need to dig deeper and understand not just what the binary wants, but also what magic value unlocks its secrets.

The flag is hidden behind multiple transformation stages and a validation check that's looking for something very specific. Put on your reverse engineering hat and show this developer that no amount of obfuscation can stop a determined CTF player!

Note: This binary was compiled for Linux x86_64. Break out your decompiler and get ready to trace through some transformation functions.

## Summary
- **Author:** Sayed Hamzah (@BaeSenseii)
- **Category:** Misc
- **Learning Objective:** Understanding multi-stage data transformations and hex value validation in reverse engineering

## Requirements
- linrev_lvl1

## Files
- [`linrev_lvl2.7z`](./dist/linrev_lvl2.7z)

## Hints
- `The binary wants TWO arguments this time. What could they be?` (200 points)
- `There's a classic hex value that shows up in a lot of security code. Think about what developers use for magic numbers...` (200 points)
- `The function names might be obfuscated, but the validation logic tells you exactly what values it's checking for.` (200 points)

## Flags
- `SPARK{0k4y_Th15_15_4_B11T_D1FF}`
