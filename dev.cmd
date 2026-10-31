@echo off
rem dev.cmd - run project commands. Plain batch, so no PowerShell execution policy
rem is involved at all (no -ExecutionPolicy Bypass needed).
rem Usage: dev.cmd lint / test / compile / run / distribute
rem        dev.cmd test <testcase>
rem SDK lookup: %RENPY_SDK% -> ..\tools\renpy-8.5.3-sdk -> ..\renpy-8.5.3-sdk
rem Only explicit paths and the two fixed folders next to the repo are accepted;
rem drive roots are not scanned, so a planted renpy.py cannot be picked up.
setlocal EnableExtensions

set "REPO=%~dp0"
set "REPO=%REPO:~0,-1%"
set "CMD=%~1"
if "%CMD%"=="" set "CMD=lint"

set "SDK="
if not "%RENPY_SDK%"=="" if exist "%RENPY_SDK%\renpy.py" set "SDK=%RENPY_SDK%"
if not defined SDK if exist "%REPO%\..\tools\renpy-8.5.3-sdk\renpy.py" set "SDK=%REPO%\..\tools\renpy-8.5.3-sdk"
if not defined SDK if exist "%REPO%\..\renpy-8.5.3-sdk\renpy.py" set "SDK=%REPO%\..\renpy-8.5.3-sdk"
if not defined SDK goto :nosdk

set "PY=%SDK%\lib\py3-windows-x86_64\python.exe"
echo SDK : %SDK%
echo repo: %REPO%
echo cmd : %CMD%

if /i "%CMD%"=="run" goto :dorun
if /i "%CMD%"=="test" goto :dotest

"%PY%" "%SDK%\renpy.py" "%REPO%" %CMD%
exit /b %ERRORLEVEL%

:dorun
"%SDK%\renpy.exe" "%REPO%"
exit /b %ERRORLEVEL%

:dotest
if "%~2"=="" (
    "%PY%" "%SDK%\renpy.py" "%REPO%" test
) else (
    "%PY%" "%SDK%\renpy.py" "%REPO%" test %~2
)
exit /b %ERRORLEVEL%

:nosdk
echo Ren'Py 8.5.3 SDK not found.
echo Download: https://www.renpy.org/dl/8.5.3/renpy-8.5.3-sdk.zip  (unzip, no install)
echo Then either:  set RENPY_SDK=D:\renpy-8.5.3-sdk
echo or put it at:  %REPO%\..\tools\renpy-8.5.3-sdk
exit /b 1
