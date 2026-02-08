@echo off
setlocal enabledelayedexpansion

echo =========================================
echo    Ateru Pipeline Setup (Windows)
echo =========================================

:: Configuración para evitar errores de hardlink en Dropbox/Unidades de Red
set "UV_LINK_MODE=copy"

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

:: Sincronizar con modo copia para evitar errores de permisos en Dropbox
uv sync --link-mode=copy

set "BIN_DIR=%USERPROFILE%\.local\bin"
if not exist "%BIN_DIR%" mkdir "%BIN_DIR%"

set "ATERU_BAT=%BIN_DIR%\ateru.bat"

echo [+] Creating global bin: %ATERU_BAT%

(
echo @echo off
echo setlocal
echo :: forcing PYTHONPATH to root for skip ModuleNotFoundError
echo set "PYTHONPATH=%PIPELINE_ROOT%;%%PYTHONPATH%%"
echo cd /d "%PIPELINE_ROOT%"
echo :: running uv for entry point 'ateru'
echo uv run ateru %%*
) > "%ATERU_BAT%"

set "SAFE_BIN_DIR=%USERPROFILE%\.local\bin"

:: Agrega al PATH y refresca la sesión actual de esta terminal
powershell -Command ^
    "$userPath = [Environment]::GetEnvironmentVariable('Path','User'); ^
    if($userPath -notlike '*%SAFE_BIN_DIR%*'){ ^
        [Environment]::SetEnvironmentVariable('Path', $userPath + ';%SAFE_BIN_DIR%', 'User'); ^
        Write-Host '[OK] %SAFE_BIN_DIR% added to PATH Registry.'; ^
    } ^
    $env:Path = [System.Environment]::GetEnvironmentVariable('Path','User') + ';' + [System.Environment]::GetEnvironmentVariable('Path','Machine'); ^
    Write-Host '[OK] Session PATH refreshed.'"

echo.
echo =========================================
echo    INSTALLATION DONE
echo =========================================
echo [!] If 'ateru' is not recognized, please restart your terminal.
echo [!] Try typing: ateru --help
echo.
pause