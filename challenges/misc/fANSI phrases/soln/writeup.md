## Solution
Based on the description, you are meant to connect to the server via the given port. `netcat` is a good tool to use for testing the connection.

### Netcat trial
When connecting to the server via `netcat`, the server will give a response of a sentence. The sentence will be a jumble of random alphabets, spacing, and underscores of length 17 to 24 characters. Within the sentence, up to one-third of the sentence will be colored via ANSI escape codes.

If you try to type the characters and send it to the server, it'll respond with too slow. This tells you that you have to connect and send a reply automatically within the set time-limit.

### Creating a python script
A script has to be created to:
    1) Connect to the server and receive the reply
    2) Take the reply, strip the ANSI escape codes
    3) Send the stripped text back to the server
    4) Receive a reply (flag)

Creating a python script is suggested, as it is easy to use and understand. The `socket` library can be used to connect to the server [`link`](https://www.geeksforgeeks.org/python/socket-programming-python/). The `re` library is useful to strip the ANSI escape codes via regular expressions [`link`](https://www.geeksforgeeks.org/python/regular-expression-python-examples/).

## Solution
Refer to [`soln.py`](./soln.py)

## Hints
Read up on client to server connections in python, ANSI escape codes