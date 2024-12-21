# Solution

1. Using the HEX Editor, search for different variations of `50 4B 03 04`.
2. When searching using the first 3 bytes, we find the starter header is wrong: `50 4B 03 FF`
3. Change the last byte from `FF` to `04`.
4. Export the file from the HEX Editor and use a software that can Unzip Zip files and unzip the exported image to get the `flag.txt`