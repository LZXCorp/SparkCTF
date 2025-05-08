# Solution

1. Visit [cyberchef](https://gchq.github.io/CyberChef/)
2. Decode from Braille
3. Decode from Hexdump
4. Decode from Base64
5. Decode from binary
6. Use "Magic" with default depth (it will take some time, this is intentional for the purposes of making manual decryption impossible)

## Full data format conversion stack

1. To Base64
2. To Hex
3. To Binary
4. To Hex (Where participants manually decrypting will start to get stuck)
5. To Binary
6. To Base64
7. To Binary
8. To Base64
9. To Hexdump
10. To Braille

## Flag

- `SIG24{w4s_1t_n3c3s54rY_4ft3r_4ll}` (static)
