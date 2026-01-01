There might probably be other ways to go about this but here's what I did:
1. Find a hex viewer: https://hexed.it/ is what I used.
2. Open the file in Hex view, You will see the header values looks a little strange, the file is given as "file" type, we only know it's an image type file.
3. So we need to find the actual hex header values needed for this file, to check the file type, we can look at the hex trailer, we see that the value is FF D9 this means that this file is a JFIF file.
4. The header for a typical JFIF file is: FF D8 FF E0 00 10 4A 46 49 46 00 --> FF D8 = JPEG file Marker, FF E0 = APP0 marker, 00 10 = APP0 segment length, 4A 46 49 46 00= ASCII for "JFIF".
5. So after changing the headers appropriately, we can then rename the file from catflag.file to catflag.jpg
6. The image will now be view-able! and you will be able to input the flag now :>

Learn more about JPG-Signature for those confused: https://www.file-recovery.com/jpg-signature-format.htm
