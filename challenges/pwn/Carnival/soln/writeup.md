## Solution
Based on the source code, we are given 50 credits to buy tickets. However, each ticket costs 100 and we cannot top up.

What can we do?

### Integer underflow
This happens when you try to exceed **minimum** threshold that is meant for the integer type assigned to a variable. Depending on whether it is `signed` or `unsigned` integer, the results can be different.


## Two's Complement and how we can abuse this
Read this for a better idea of this concept: [Link](https://www.cs.cornell.edu/~tomf/notes/cps104/twoscomp.html)

`Signed` integers can be both positive and negative values. But with `1`s and `0`s, how can there be negative numbers?

This is because `signed` integers allocate the **upper** half of its space to negative integers.

```shell
# Short signed 2 byte integer

Bin: 0111 1111 1111 1111
Dec: 32767

Bin: 1000 0000 0000 0000
Dec: -32768

Bin: 1000 0000 0000 0001
Dec: -32767
```

But what happens if we attempt to decrement beyond `-32768`? 

This will actually result then cause a wrap around (since there is a 2 byte constraint)

```shell 
-32768 - 1 --> 32767
```

With this knowledge, let's use it for our exercise


### Vulnerability
In our source code, there is no boundary checking for number of tickets we can buy and the transcation will go through before checking, as seen below: 

```c
    balance = balance - (num_tickets * ticket_price);

    if(balance > 0) {
        printf("Your remaining balance: %d credits\n", balance);
        printf("Here's your tickets!\n");
        flag();
    } else {
        ...
    }
```

The check is also done for `balance` variable. Thi

This means we can should attempt to cause the "wrap around" by buying an enough and big number of tickets.


### Exploit
Since we want to cause the wrap around, we need to buy at least this much worth of tickets:

Current balance (30) + 32768 = 32798 credits

32798 / 100 per ticket = ~328

We need to buy at least 328 tickets

## Solution
Refer to soln.py

## Hints
1. Search up "signed integers"