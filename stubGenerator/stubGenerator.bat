rem @echo off

if not "%SY_ROOT%"=="" goto hasEnv

if "%SY_ROOT%"=="" goto noEnv

:hasEnv
%SY_TOOLS_DIR%\python\stubGenerator
python __init__.py
popd
goto end


:noEnv
PATH=%PATH%;C:\Python27
python __init__.py
pause
goto end


:end
