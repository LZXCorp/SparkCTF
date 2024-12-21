# Solution


1. Using the HEX Editor, search for different variations of `50 4B 03 04`.

2. When searching using the last 3 bytes, we find the starter header is wrong: `42** 4B 03 04`

3. Change the first byte from `42` to `50`.

4. Export the file from the HEX Editor.

5. Based on the hint, the password to the ZIP file is `Elephant`, but it still fails

6. Bruteforce using a script to try all capitalization combinations of `elephant` to find that the password to the ZIP file. For this script, I use python itertools to help me to get the 256 combinations of the word `elephant`.

```python
from itertools import product 
word = "elephant" 

# Generate all combinations of lowercase and uppercase letters for the word 
combinations = list(product(*[(c.lower(), c.upper()) for c in word])) 

# Write all combinations to a file called char.txt 
with open("char.txt", "w") as f: 
	for combo in combinations: 
		f.write("".join(combo) + "\n") 
		
print(f"Wordlist generated with {len(combinations)} combinations.")
```

7.  After that we can use fcrackzip to bruteforce our password using the dictionary that we created called char.txt to help us get the password.

```
fcrackzip -v -u -D -p char.txt <path_of_zip_file>
```

8. Password is `ElePhANt`
