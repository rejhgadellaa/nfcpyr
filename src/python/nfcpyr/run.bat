@echo off
cls

:findpy
set py=c:/python27/python.exe
if not exist %py% set py=c:/python27/python.exe
if not exist %py% set py=c:/python27/python.exe
if not exist %py% goto error

:run
call %py% nfcpyr.py
if errorlevel 10 goto run
if errorlevel 1 goto error


goto exit
:error
echo An error occured
choice /C QYN /N /T 60 /D N /M "Press 'Q' to quit"
goto end

:exit
echo.
echo.
choice /C QYN /N /T 10 /D N /M "Press 'Q' to quit"

:end