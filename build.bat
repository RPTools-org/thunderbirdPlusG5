@echo off
title=Build Thunderbird+G5 x64
rem set srcDir=%~dp0thunderbirdPlusG5

rem d:
rem cd %srcDir%
rem echo %srcDir%
rem pause
echo construction
call scons -s
move *.nvda-addon ..
echo cleaning
call scons -c
cd ..
set /p r=Press enter to close