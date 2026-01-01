## Solution
Work from the top of the python script downwards, then use either online tools or python to reverse what was done on the output flag given

# Understanding the script
1. We see that binascii was imported, we can head to the binascii documentation page if unfamiliar with the module.
2. there is a character list, something some ciphers typically use, so looking at the encrypt function we can see that it is for a ceaser cipher, as characters are shifted based on a key value.
3. So next we see that the flag is further encrypted after the ceaser cipher, the ceaser output is converted into a hex in line 25, and then converted into binary in line 26.
# Solving the Challenge
1. So first we can put the flag output given into a binary to hexadecimal converter I used: https://www.rapidtables.com/convert/number/binary-to-hex.html
2. Next we convert the hexadecimal to text to get the ciphertext, I used: https://www.rapidtables.com/convert/number/hex-to-ascii.html
3. We can then use a ceaser cipher decoder online: https://cryptii.com/pipes/caesar-cipher
4. In the ceaser cipher decoder, replace the alphabet list with the one in the python document, then cycle through the shifts until the flag is decipherable! 
