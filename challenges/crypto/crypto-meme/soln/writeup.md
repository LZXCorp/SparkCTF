In the "crypto-meme.txt" file, we are able to identify that it is RSA. However, something weird is that the e value is 3, a value too low for RSA to work properly especially when the N value is significantly large.
Hence, all we have to do is get the cube root of the encrypted value and convert it to byte value (i.e. using Cryptodome's long_to_bytes method to get the flag)
