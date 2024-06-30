@echo on
setlocal EnableDelayedExpansion

forfiles /c "cmd /c if @isDir == FALSE pushd %~dp0 && whiskers @path" /m "*.tera" /p ".\src" /s & exit

for /f %%a in ('forfiles /c "cmd /c if @isDir == TRUE echo @path" /p ".\dist"') do (
  set "_FILES="
  for /f "delims=" %%b in ('forfiles /c "cmd /c if @isDir == FALSE echo @relpath" /p "%%a" /s') do ( set "b=%%b" && set "_FILES=!_FILES! !b:~3,-1!" )
  set "FILES=!_FILES:~1!"
  tar --create --directory "%%a" --file "%%a.tar.gz" --gzip !FILES!
)
