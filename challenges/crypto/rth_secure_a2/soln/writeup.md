# Solution

1. Factorize *n* to get *p* and *q*, using the quadratic sieve method.
$$
p=1312724141395542719846067182351937200087968421399 \\
q=254533367464781663728670476767351829873
$$

2. Rewrite the encryption formula to isolate $m^e$ as itself.
$$
c = (m^e + k)\mod n \\
c ≡ m^e + k \pmod n \\
c - k ≡ m^e \pmod n \\
m^e ≡ (c - k) \mod n
$$

3. From the decryption formula, we can expand it such that $m = ((c-k) \mod{n})^k\mod{n}$. From there we can insert $m^e$ into the equation.
$$
m = (m^e)^k\mod{n}
$$

4. Next, calculate the value of *k* using:
$$
k= \lfloor {n - p^e \mod n \over 2} \rfloor
$$

5. Take the value in `encrypted.txt` as *c* and use the decryption equation to calculate for the value of *m*.

6. Once the value of *m* is calculated, use the converter, [numbertoflag.py](../dist/numbertoflag.py) to convert the *m* value to a string, which will be your flag.