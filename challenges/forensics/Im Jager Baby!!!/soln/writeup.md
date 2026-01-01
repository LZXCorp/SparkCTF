## Solution
To solve this, the image must be open in a NTFS Windows machine to see the ADS data.

Once you see it, run the following command to help you view the data in the JPEG file

```
dir /r <file path of image>
```

There is a total of 300 stream files. Whats important is the content in the stream file. To do this, we can easily generate a powershell script to help us automate and find our flag. 

```
# === CONFIGURATION ===
$mainFile = "<file path>"

# === SCAN AND DECODE FLAG ===
$streams = Get-Item -Path $mainFile -Stream * | Where-Object { $_.Stream -like "flag*.txt" }

foreach ($s in $streams) {
    try {
        # Read entire stream as a single string
        $content = Get-Content -Path "${mainFile}:$($s.Stream)" -Raw -ErrorAction Stop

        # Decode Base64
        $decodedBytes = [System.Convert]::FromBase64String($content)
        $decodedText = [System.Text.Encoding]::UTF8.GetString($decodedBytes)

        # Check if it contains your expected flag pattern
        if ($decodedText -like "SPARK*") {
            Write-Output "[+] Found flag in stream $($s.Stream):"
            Write-Output $decodedText
        }
    } catch {
        # Ignore streams that fail to decode
    }
}
```


