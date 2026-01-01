# Solution
There are probably other ways to do this but this is what we did and used:
1. Use wireshark to open the pcap file, and look through the packets to find any possible credentials hidden in the packets.
2. In Packet 3 and 359 there will be a Linux shadow file entry: tom:$y$j9T$z4IEbdYbmdgJEAffgoZSd.$C4Qd9y.TKajo4RVQ6dWp3VX2lG3aG3YRaZzaEpXag05:20348:0:99999:7:::
3. From this entry we can find out that the user account's username is tom and the password is probably in $y$j9T$z4IEbdYbmdgJEAffgoZSd.$C4Qd9y.TKajo4RVQ6dWp3VX2lG3aG3YRaZzaEpXag05
4. $y$ in the entry shows that this is a yescrypt hash :).
5. So we can take the hash and use john the ripper, to try to decrypt it. 
6. Using the provided rockyou.txt should be enough to decrypt this password. (password is sparky)
7. Heading over to the website, we will see that it is a simple login page, input the credentials found earlier: Username: tom, Password: sparky.
8. You will now see the flag! yay! 
