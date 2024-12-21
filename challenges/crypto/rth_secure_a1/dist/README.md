Prime numbers are used a lot in cryptography.

RSA, which uses Public Key Cryptography, makes use of the multiplication of prime numbers, *p* and *q*, to generate the value *n*.

Your objective is to decrypt the list of values in `encrypted.txt`.
Make use of the resources you are provided here, it should be a piece of cake.
You should take each item in the list as it's own value *c* for calculation.

The RSA Decryption formula is: $m = c^dpmod n$
The calculation of *d* is $dcdot epmod{\phi(n)}=1$,
where $\phi$ is $(p-1)(q-1)$

You are provided with some of the values for decryption in `rth.txt`.

The flag (decimal form) should look exactly like this:
XX XX XX XX XX XXX XXX XX XXX XXX XX XXX XX XX XX XXX XXX

You may make use of `rth-check.py` to check that your answer is in the right format.

For more information regarding RSA, look no further than the [CTF101 Website](https://ctf101.org/cryptography/what-is-rsa/)!

FactorDB: https://factordb.com/
CyberChef (From Decimal): https://gchq.github.io/CyberChef/#recipe=From_Decimal('Space',false)