## Solution
There are multiple ways to do this. But one of the tools that I managed to learn was the ZimmermanTools that contains "MFTECmd.exe". 

This tool allows you to parse a MFT table and provide you useful informations such as file paths, extensions and also the creation time, modified time etc.

1) Download the tools from https://ericzimmerman.github.io/#!index.md. The powershell script is safe to use.
2) Do the necessary installations and go to the folder which contains MFTECmd.exe.
3) Run the following command - .\MFTECmd.exe -f _path of MFT table_ --csv _path where you want to put the csv file_
4) Scroll through the CSV file and find the relevant file. :)

