# Solution

1. There are two parts to this flag, the first is making use of LSB and another making use of Amplitude Modulation.

### PART 1: LEAST SIGNIFICANT BIT (LSB)

2. The first half of the flag is hidden with the audio samples.
3. An **audio sample** is **a value**, and every second has *n* samples, where *n* is the **audio's sample rate**.
4. Each of the audio samples can be converted into a binary value.

```
SAMPLE 1: 77 -> 0100 1101
SAMPLE 2: 36 -> 0010 0100
SAMPLE 3:  0 -> 0000 0000
...
SAMPLE 8: 46 -> 0010 1110
```

5. Take a look at these unmodified samples, the last significant bit (LSB) concept takes the bit which changes the value the least.

6. In this case, it is the last bit of a binary.

7. The flag is encoded at the end of the LSB in ASCII as binary.

8. For instance, take the letter `N` -> 0100 1110. We change the LSB of the first 8 samples to match up with the ASCII binary of `N`

```
SAMPLE 1: 76 -> 0100 1100
SAMPLE 2: 37 -> 0010 0101
SAMPLE 3:  0 -> 0000 0000
...
SAMPLE 8: 46 -> 0010 1110
```

9. Now to decode for every sample to get the first half of the flag.


### PART 2: AMPLITUDE MODULATION

10. This uses the same concept as the previous flag, encoding ASCII characters into the audio, but instead for amplitude.

11. Analysing the audio data reveals that some portions of the audio has lower amplitude while other parts have higher amplitudes.
![spec_amp](spec_amp.png)

12. Instead of taking the peak amplitude, we take the average amplitude of each interval, which is a second.

13. After that, compare it to a threshold of your choice based on your analysis of the amplitude. If the average amplitude is lesser or equal to the threshold, make it a bit '1', else '0'.

14. After that, transform the bit array to a byte array, then convert each byte into an ASCII character.

15. Combining the ASCII characters will give you the second half of the flag.


### FINAL STEP

16. Combine both parts together to construct the flag