# Solution

1. Open the Phantom Page in your browser (the running service).
2. Open Developer Tools → **Network** (or use View Source + look for loaded assets).
3. Locate the hidden script asset (e.g. `GET /assets/ghost.js`) that the page loads.
4. Open `/assets/ghost.js` and find the array of string shards (the script contains many small base64-like fragments).
5. Concatenate the shards into one base64 string. For example, if the script shows:

```js
const fragment_a = ["U1BB", "Ukt7", "ajNf", "bDBv"];
const fragment_b = ["a3Nf", "YTJl", "X2Rl", "YzNp"];
const fragment_c = ["dmk0", "Z30="];
```
join them into a single string (no separators), e.g.:

```
U1BBUkt7ajNfbDBva3NfYTJlX2RlYzNpdmk0Z30=
```

6. Base64-decode the concatenated string. You can do this with Python or a command-line tool.

**Python (recommended):**
```
python3 - <<'PY'
import base64
b64 = "U1BBUkt7ajNfbDBva3NfYTJlX2RlYzNpdmk0Z30="
print(base64.b64decode(b64).decode())
PY
```

**Or Node.js:**
```
node -e "console.log(Buffer.from('U1BBUkt7ajNfbDBva3NfYTJlX2RlYzNpdmk0Z30=','base64').toString())"
```

**Or (if on a Unix-like system) with base64/openssl:**
```
echo 'U1BBUkt7ajNfbDBva3NfYTJlX2RlYzNpdmk0Z30=' | base64 --decode
```
# Or
```
echo 'U1BBUkt7ajNfbDBva3NfYTJlX2RlYzNpdmk0Z30=' | openssl base64 -d 
```
The decoded result will be the secret token string (the challenge’s inner text). For this challenge the decoded token is:

```
j3_l0oks_a2e_dec3ivi4g
```

7. Format the flag with the SPARK prefix and braces and submit:

```
SPARK{j3_l0oks_a2e_dec3ivi4g}
```
