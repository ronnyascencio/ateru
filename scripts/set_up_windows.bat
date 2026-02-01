@echo off
setlocal enabledelayedexpansion

echo =========================================
echo    Xolo Pipeline Setup (Windows)
echo =========================================


set "PIPELINE_ROOT=%~dp0.."
for %%i in ("%PIPELINE_ROOT%") do set "PIPELINE_ROOT=%%~fpi"
set "SYSTEM_ROOT=%SystemDrive%\"

echo [+] PIPELINE_ROOT: %PIPELINE_ROOT%


setx PIPELINE_ROOT "%PIPELINE_ROOT%" > nul
setx SYSTEM_ROOT "%SYSTEM_ROOT%" > nul


where uv >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [!] uv not found. Installing uv...
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    set "PATH=%USERPROFILE%\.cargo\bin;%PATH%"
) else (
    echo [OK] uv already installed.
)


cd /d "%PIPELINE_ROOT%"
echo [+] sync dependences and registring project...

uv sync


set "BIN_DIR=%USERPROFILE%\.local\bin"
if not exist "%BIN_DIR%" mkdir "%BIN_DIR%"

set "XOLO_BAT=%BIN_DIR%\xolo.bat"

echo [+] Creating global bin: %XOLO_BAT%

(
echo @echo off
echo setlocal
echo :: forcing  PYTHONPATH to root for skip ModuleNotFoundError
echo set "PYTHONPATH=%PIPELINE_ROOT%;%%PYTHONPATH%%"
echo cd /d "%PIPELINE_ROOT%"
echo ::running uv for  entry point 'xolo'
echo uv run xolo %%*
) > "%XOLO_BAT%"


set "SAFE_BIN_DIR=%USERPROFILE%\.local\bin"
powershell -Command "$p=[Environment]::GetEnvironmentVariable('Path','User'); if($p -notlike '*%SAFE_BIN_DIR%*'){ [Environment]::SetEnvironmentVariable('Path',$p+';%SAFE_BIN_DIR%','User'); echo '[OK] %SAFE_BIN_DIR% agregado al PATH.' } else { echo '[OK] directory already in PATH.' }"

echo.
echo =========================================
echo    INSTALLATION DONE
echo =========================================
echo [!]IMPORTANT CLOSE AND REOPEN THE TERMINAL.
echo [!] Try typing in terminal: xolo --help
echo.
pause
