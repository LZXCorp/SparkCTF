# Solution

1. Open `dist/manuscript.txt` and read through the whimsical story carefully.
2. Notice that the puzzle hints mention **punctuation** and that the secret key is hidden as a **word directly before a question mark**.
3. Search the story for sentences ending with a question mark (`?`).
4. Identify the word immediately before the question mark in that sentence.  
   - In this story:  
     ```
     Never forget to wonder what ForestKeyAdventurer? could mean as you read.
     ```
   - The word before `?` is: `ForestKeyAdventurer`
5. This is the **secret key** to decrypt the treasure.
6. Decrypt the encrypted file using OpenSSL: 
```bash
openssl enc -d -aes-256-cbc -in dist/treasure.enc -out flag.txt -pass pass:ForestKeyAdventurer
```
7. Open flag.txt to retrieve the flag: SPARK{y0u_h4v3_f0u4d_t4e_tr34s7r3}
