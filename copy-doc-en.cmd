@echo off
if not exist .\addon\doc\en (
	md .\addon\doc\en
copy .\doc-en\readme.md
copy .\doc-en\keyEquiv_en.md
copy .\doc-en\*.* .\addon\doc\en 
	)

