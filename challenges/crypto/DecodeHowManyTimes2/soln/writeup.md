# Solution

1. Create the Base64 Decoding function.
2. Create a while loop that loops until the start of the decoded string is 'SIG24'. (Optional: Include a max number of loops to ensure it does not do it forever, but it should error out if it can't decode so this is optional.)
3. The solution script is located here: [](./broad_ch2_solution.py)
4. Now after decoding all of that, you should get `SIG24{KNEUO63OGB3V6MLNL52GQM27OJSWCMK7GF6Q====}`
5. When looking at the number of times you decoded, you decoded 32 times.
6. Use a Base32 Decoder to decode the above string to get the actual flag.