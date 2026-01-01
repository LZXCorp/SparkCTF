# What Do You Mean? (Solution)

## Challenge Overview
**Category:** Cryptography
**Challenge:** Decrypt the message: `fjw gmktt lrt gyl ftptr ojpt lrt rjrt`

## Initial Analysis

This is a classic substitution cipher challenge. The encrypted message consists of several words, and we need to determine what they represent.

Given the challenge context and the nature of the ciphertext, we can hypothesize that each word represents a digit spelled out in English (zero through nine).

## Solution Methodology

### Step 1: Identify the Number Spellings

First, let's list all possible English spellings for digits 0-9:
- **0:** zero (4 letters)
- **1:** one (3 letters)
- **2:** two (3 letters)
- **3:** three (5 letters)
- **4:** four (4 letters)
- **5:** five (4 letters)
- **6:** six (3 letters)
- **7:** seven (5 letters)
- **8:** eight (5 letters)
- **9:** nine (4 letters)

### Step 2: Analyze Word Patterns

Let's examine the encrypted message structure:
```
fjw gmktt lrt gyl ftptr ojpt lrt rjrt
```

Breaking down by word length:
- **3-letter words:** `fjw`, `lrt`, `gyl`, `lrt`
- **4-letter words:** `ojpt`, `rjrt`
- **5-letter words:** `gmktt`, `ftptr`

### Step 3: Pattern Matching - 5-Letter Words

The 5-letter number spellings are: **three**, **seven**, and **eight**.

Looking at `gmktt`:
- Pattern: `X-Y-Z-Y-Y` (letter at positions 3, 4, 5 repeat)
- Only **"three"** fits this pattern: `t-h-r-e-e`
- **Mapping discovered:** `g→t`, `m→h`, `k→r`, `t→e`

Looking at `ftptr`:
- Pattern: `X-Y-Z-Y-W`
- With known mappings: `?-e-?-e-?`
- This matches **"seven"**: `s-e-v-e-n`
- **Mapping discovered:** `f→s`, `p→v`, `r→n`

### Step 4: Deducing 3-Letter Words

Now we know: `g→t`, `k→r`, `t→e`, `f→s`, `p→v`, `r→n`

For `lrt`:
- Using `r→n` and `t→e`: `l-n-e`
- This matches **"one"**
- **Mapping discovered:** `l→o`

For `fjw`:
- Using `f→s`: `s-?-?`
- The only 3-letter number starting with 's' is **"six"**
- **Mapping discovered:** `j→i`, `w→x`

For `gyl`:
- Using `g→t` and `l→o`: `t-?-o`
- This matches **"two"**
- **Mapping discovered:** `y→w`

### Step 5: Deducing 4-Letter Words

For `ojpt`:
- Using `j→i`, `p→v`, `t→e`: `?-i-v-e`
- This matches **"five"**
- **Mapping discovered:** `o→f`

For `rjrt`:
- Using `r→n`, `j→i`, `t→e`: `n-i-n-e`
- This matches **"nine"**

### Step 6: Complete Decryption

Now we can decrypt the entire message:

```
fjw   → six   (6)
gmktt → three (3)
lrt   → one   (1)
gyl   → two   (2)
ftptr → seven (7)
ojpt  → five  (5)
lrt   → one   (1)
rjrt  → nine  (9)
```

## Final Substitution Mapping

```
Cipher: f  g  j  k  l  m  o  p  r  t  w  y
Plain:  s  t  i  r  o  h  f  v  n  e  x  w
```

## Answer

Concatenating the decrypted digits: **6-3-1-2-7-5-1-9**, submit the flag by connecting to the port and you should be able to get the answer: 
``SPARK{01d_bUt_g0ld_cRypt0}``
