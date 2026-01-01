## INTENDED SOLVING STEPS

1. This requires the use of a steganography analysis tool. Particularly one that supports anlaysing images by their Bit Planes and Colour Channels.
2. A tool I've used is 'stegsolve.jar' (https://kb.offsec.nl/tools/forensics/stegsolve). 
3. Stegsolve can run on Windows too, but Im using Kali. *Remember to give the file Executable permissions (chmod +x stegsolve.jar)*.
4. Run the 'stegsolve.jar' GUI using this command "java -jar stegsolve.jar". 
5. Open your PNG file into the GUI, and cycle through the Bit planes (colour channels?).
6. The Flag should be easily indentifiable in the Blue Plane 0.

Note: The png is not too large, so Online tools like https://aperisolve.fr, can easily automate many steganography analysis quickly.

## FLAG

`SPARK{blu3_b1t_pl4ne_LSB}`