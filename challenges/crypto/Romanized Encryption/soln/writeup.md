## Solution
Based on the description, you are meant to connect to the server via the given port. `netcat` is a good tool to use for testing the connection.

### Netcat trial
When connecting to the server via `netcat`, the server will give a response of a sentence. The sentence will be a jumble of random alphabets. When you send a response via typing, it'll say 'Wrong answer. Try again.', and after 10 seconds, it'll disconnect the session and respond with too slow. 

With this knowledge, you will come to the conclusion that you are supposed to brute force till the answer is correct. As for what to bruteforce, its using the Caesar Cipher, with a big hint given in the challenge description about ancient romes dictator Julius Caesar.

### Creating a python script
A script has to be created to:
    1) Connect to the server and receive the reply
    2) Take the reply, and come up with all possible shifts.
    3) Send the shifted text back to the server one by one.
    4) Receive a positive reply (flag)

Creating a python script is suggested, as it is easy to use and understand. The `socket` library can be used to connect to the server [`link`](https://www.geeksforgeeks.org/python/socket-programming-python/).

## Solution
Refer to [`soln.py`](./soln.py)

## Hints
Read up on client to server connections in python, Caesar Cipher