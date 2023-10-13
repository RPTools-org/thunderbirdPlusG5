@echo off
title Build Thhunderbird+ add-on


rem if exist .\addon\buildVars.py (
rem 	copy .\addon\buildVars.py .
rem 	)
ECHO COPY DOC_EN
call copy-doc-en.cmd
ECHO CONSTRUCT
call scons -s
SET /P PR=Press Enter to continue...
ren *.nvda-addon *.nvda-addonTMP
call scons -c
ren *.nvda-addonTMP *.nvda-addon 
del /s /q *.pyc > NUL
del .sconsign.dblite> NUL
rd /s  /q __pycache__
rd /s /q  .\site_scons\site_tools\gettexttool\__pycache__
call copy-doc-en.cmd
