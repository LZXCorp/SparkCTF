# Solution

1. We know the that the file is of type PNG, so it should have a file signature of `89 50 4E 47 0D 0A 1A 0A`.
2. When searching using the last 3 bytes, we find the file signature is wrong: `89 51 4F 49 10 0F 22 17`
3. When looking at the difference between both, we get this (in decimal form): `0 1 1 2 3 5 8 13`.
4. This resembles the fibonacci sequence, which is what this file was encrypted with.
5. Make use of Python to create a script to help in the decryption of the file. [file_decryptfib.py](./file_decryptfib.py)
6. Open the decrypted image file to get the flag.