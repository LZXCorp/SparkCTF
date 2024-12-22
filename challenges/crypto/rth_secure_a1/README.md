# rth_secure_a - Flag 1

Prime numbers are used a lot in cryptography.

RSA, which uses Public Key Cryptography, makes use of the multiplication of prime numbers, *p* and *q*, to generate the value *n*.

Your objective is to decrypt the list of values in `encrypted.txt`.
Make use of the resources you are provided here, it should be a piece of cake.
You should take each item in the list as it's own value *c* for calculation.

Make use of `README.md` to get the **Full Description** of this challenge.

FactorDB: https://factordb.com/
CyberChef (From Decimal): https://gchq.github.io/CyberChef/#recipe=From_Decimal('Space',false)

## Summary
- **Author:** Zhen Xiang
- **Category:** Cryptography
- **Difficulty:** Easy
- **Solution Writeup:** [`writeup.md`](./soln/writeup.md)

## Hints
- `n is p*q, both values are prime numbers. What method can be used to divide n into it's individual prime factors?` (100 Points)

## Files
- [`encrypted.txt`](./dist/encrypted.txt)
- [`README.md`](./dist/README.md)
- [`rth-check.py`](./dist/rth-check.py)
- [`rth.txt`](./dist/rth.txt)

## Flags
- `SIG24{t1e_rTh_tErm_fUn_rS3}`
