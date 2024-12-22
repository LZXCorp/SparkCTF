# Solution

1. The only provided values were *n* and *e*, which is the public key used for the encryption. The private key makes use of the totient of the prime factors of *n*.
2. The provided resource, [FactorDB](https://factordb.com/) is used to factorize the value of *n* to it's prime factors, 59 and 97.
3. Using this, we can calculate for the value of *d*.

```math
\phi = (59-1)(97-1) = 5568 \\
d \cdot e \pmod{5568} = 1 \\
d = 5021
```

4. Now we have all the values to calculate the decrypted message for the given formula, $m = c^d \mod n$.
5. Create a script to decrypt each value and convert it from decimal to ASCII to get the flag. An solution script has been created: [rth-soln.py](./rth-soln.py)
