@echo off

if "%MAYA_SCRIPT_PATH%"=="" goto SetVars
rem if not "%MAYA_SCRIPT_PATH%"=="" goTo CheckForEnv




:CheckForEnv
if not "%MAYA_DIR%"=="" goto hasEnv
if "%MAYA_DIR%"=="" goto notThroughEnv


rem if "%MAYA_DIR%"=="" set maya_exe=C:\Program Files\Autodesk\Maya2011\bin

rem if not "%MAYA_DIR%"=="" set maya_exe=%MAYA_DIR%bin

:notThroughEnv
set maya_exe=C:\Program Files\Autodesk\Maya2011\bin
set menu_dir=%~dp0
set menu_dir=%menu_dir:\maya\=%
set menu_dir=%menu_dir%\maya\createMenu.mel
RED Lab should be using Python27
set PATH=%PATH%;C:\Python27
pushd %maya_exe%
goto StartMaya



:hasEnv
set maya_exe=%MAYA_DIR%bin
set menu_dir=%~dp0
set menu_dir=%menu_dir:\maya\=%
set menu_dir=%menu_dir%\maya\createMenu.mel
pushd %maya_exe%
goto StartMaya


:SetVars
SET current_dir=%~dp0
SET tools_dir=%current_dir:\maya\=%
rem SET current_dir=
rem SET tools_dir=%tools_dir%\Environment
pushd %tools_dir%

Set SY_TOOLS_DIR=%tools_dir%
set MECHBRAWLER_TOOLS_DIR=%tools_dir%
set SY_ASSET_DIR=%tools_dir%
set SY_ROOT=%tools_dir%\..
set SCRAPYARD_ROOT=%SY_ROOT%


set XBMLANGPATH=%tools_dir%\maya\icons

set MAYA_SCRIPT_PATH=%MAYA_SCRIPT_PATH%;%tools_dir%\maya\scripts
set MAYA_SCRIPT_PATH=%MAYA_SCRIPT_PATH%;%tools_dir%\maya\scripts\art
set MAYA_SCRIPT_PATH=%MAYA_SCRIPT_PATH%;%tools_dir%\maya\scripts\character
set MAYA_SCRIPT_PATH=%MAYA_SCRIPT_PATH%;%tools_dir%\maya\scripts\design
set MAYA_SCRIPT_PATH=%MAYA_SCRIPT_PATH%;%tools_dir%\maya\scripts\misc
set MAYA_SCRIPT_PATH=%MAYA_SCRIPT_PATH%;%tools_dir%\maya\shelves
set MAYA_SCRIPT_PATH=%MAYA_SCRIPT_PATH%;%tools_dir%\maya\source
set MAYA_SCRIPT_PATH=%MAYA_SCRIPT_PATH%;%tools_dir%\maya\source\TestPlugin
set MAYA_SCRIPT_PATH=%MAYA_SCRIPT_PATH%;%tools_dir%\maya\source\TestPlugin\TestPlugin

set MAYA_SCRIPT_PATH=%MAYA_SCRIPT_PATH%;%tools_dir%\python\emailDecorator
set MAYA_SCRIPT_PATH=%MAYA_SCRIPT_PATH%;%tools_dir%\python\perforce
set MAYA_SCRIPT_PATH=%MAYA_SCRIPT_PATH%;%tools_dir%\python\stubGenerator
set MAYA_SCRIPT_PATH=%MAYA_SCRIPT_PATH%;%tools_dir%\python\utils
rem need to change this after testing is done
SET MAYA_SCRIPT_PATH=%MAYA_SCRIPT_PATH%;%tools_dir%\Python27
SET MAYA_SCRIPT_PATH=%MAYA_SCRIPT_PATH%;%tools_dir%\Python27\Lib\site-packages


set PYTHONPATH=%tools_dir%\maya\icons
set PYTHONPATH=%PYTHONPATH%;%tools_dir%\maya\scripts
set PYTHONPATH=%PYTHONPATH%;%tools_dir%\maya\scripts\art
set PYTHONPATH=%PYTHONPATH%;%tools_dir%\maya\scripts\character
set PYTHONPATH=%PYTHONPATH%;%tools_dir%\maya\scripts\design
set PYTHONPATH=%PYTHONPATH%;%tools_dir%\maya\scripts\misc
set PYTHONPATH=%PYTHONPATH%;%tools_dir%\maya\shelves
set PYTHONPATH=%PYTHONPATH%;%tools_dir%\maya\source
set PYTHONPATH=%PYTHONPATH%;%tools_dir%\maya\source\TestPlugin
set PYTHONPATH=%PYTHONPATH%;%tools_dir%\maya\source\TestPlugin\TestPlugin

set PYTHONPATH=%PYTHONPATH%;%tools_dir%\python\emailDecorator
set PYTHONPATH=%PYTHONPATH%;%tools_dir%\python\perforce
set PYTHONPATH=%PYTHONPATH%;%tools_dir%\python\stubGenerator


SET PYTHONPATH=%PYTHONPATH%;%tools_dir%\Python27
SET PYTHONPATH=%PYTHONPATH%;%tools_dir%\Python27\Lib\site-packages
SET MAYA_SHELF_PATH=%tools_dir%\Maya\shelves
goto CheckForEnv

:StartMaya
REM the env check is also being done in the python script
start pythonw %SY_TOOLS_DIR%\maya\LaunchMaya.py
REM start maya -script %menu_dir%
popd



