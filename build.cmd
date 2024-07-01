@echo on
setlocal EnableDelayedExpansion

whiskers .\templates\settings.json.tera || exit /b 1
whiskers .\templates\themes.json.tera || exit /b 1

for /f %%a in ('forfiles /c "cmd /c if @isDir == TRUE echo @path" /p ".\dist"') do (
  set "_FILES="
  for /f "delims=" %%b in ('forfiles /c "cmd /c if @isDir == FALSE echo @relpath" /p "%%a" /s') do ( set "b=%%b" && set "_FILES=!_FILES! !b:~3,-1!" )
  set "FILES=!_FILES:~1!"
  tar --create --directory "%%a" --file "%%a.tar.gz" --gzip !FILES!
)
