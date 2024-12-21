Oh right! I can place this here for you to help me test it out. \
Basically, the new formula I am using is c=[(m^e+k)(mod n)], where *k* is a calculated number which was added :).

Then of course, to get the message back you need to decrypt it by using this formula right here: m=[(c−k)^d](mod n).

You might also be wondering how the messages are encoded/decoded for me to stuff it in. The characters are converted to bytes, then after that it is converted to [long format](https://dnmtechs.com/converting-variable-sized-byte-arrays-to-integer-long-in-python-3/). Doing the reverse gets back the message for you.

The script `numbertoflag.py` will be provided to you to simplify the conversion process.

As for *k*, it was carefully chosen to ensure that $p^e$ remains in the confines of *n*.

$$
k= \lfloor {n - p^e \mod n \over 2} \rfloor
$$