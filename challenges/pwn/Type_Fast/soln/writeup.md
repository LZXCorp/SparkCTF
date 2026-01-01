# Solving Steps

- So we can see that you need to beat the WPM record which is 5067 WPM. So that is not humnaly possible.

- Seeing the source file, we can observe there's no canary stack (im not at that lvl yet) and no PIE addresses r fixed.

- doing a simple `objdump -d chall | grep "<win>:"` to get the win() address will get us the... win address! Why? Because the win() function opens flag.txt!

- looking at the source code... we can see the buffer is only 64 bytes but read() accepts up to 256 bytes.

- we can see strcmp checks the typing phrase

- so in the your solving script, you should keep these in mind:

 - send correct typing phrase first to pass strcmp check

- add a null terminator to terminate the string properly

- pad to offset '72' to reach the return address

- overwrite return address with win addr

- when challenge func returns, it jumps to win instead of main

FLAG:  - `SPARK{w0w_v3ry_C0ol_sTu1f}`