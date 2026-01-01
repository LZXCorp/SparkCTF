## Solution
You can use whatever it is needed to parse the USN Journal data but for me, I choose to a batch script instead. 

```
@echo off
setlocal enabledelayedexpansion

:: --- CONFIGURATION ---
set "filename=SpArK.txt"
set "drive=E:"
if not "%~1"=="" set "drive=%~1"

:: Output CSV file
set "csvfile=%~dp0USN_%filename%_%date:~-4%%date:~4,2%%date:~7,2%_%time:~0,2%%time:~3,2%%time:~6,2%.csv"
set "csvfile=!csvfile: =0!"
set "tempcsv=%temp%\usn_temp_%random%.csv"

:: --- CORE EXPORT ---
fsutil usn readjournal %drive% csv > "%tempcsv%"

:: Create CSV with header
echo USN,FileReferenceNumber,ParentFileReferenceNumber,FileName,Reason,TimeStamp,FileAttributes,RemainingExtents,SourceInfo,SecurityId > "%csvfile%"

:: Filter by filename and append
findstr /i "%filename%" "%tempcsv%" >> "%csvfile%"

:: Cleanup temporary file
if exist "%tempcsv%" del "%tempcsv%" 2>nul

echo CSV export completed: %csvfile%
pause

```


