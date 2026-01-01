## INTENDED SOLVING STEPS

1. Exiftool the bread image, and you should see an embedded PDF file.
2. Using the command binwalk --dd="pdf:pdf" bread.png to extract the PDF file.
3. PDF file is password protected, so using 'pdf2john' we can pull the password hash out. 
4. Using that password hash, we use 'john' (JTR) to break it, which should give the password: tetoteto.
5. PDF contents hints to look somewhere else; like PDF's metadata. 
6. Use the cracked passphrase to view the 'Creator' of the PDF file to find the flag.

## FLAG

`SPARK{W3ak_pr0tectedf1les}`