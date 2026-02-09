@echo off
setlocal enabledelayedexpansion

echo =========================================
echo    Ateru Pipeline Setup (Windows)
echo =========================================

:: Configuración para evitar errores de hardlink en Dropbox
set "UV_LINK_MODE=copy"

:: Obtener la ruta absoluta de la raíz
pushd "%~dp0.."
set "PIPELINE_ROOT=%CD%"
popd
set "SYSTEM_ROOT=%SystemDrive%\"

echo [+] PIPELINE_ROOT: %PIPELINE_ROOT%

:: Guardar variables de entorno de usuario
setx PIPELINE_ROOT "%PIPELINE_ROOT%" > nul
setx SYSTEM_ROOT "%SYSTEM_ROOT%" > nul

:: Verificar si uv existe
where uv >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [!] uv not found. Installing uv...
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    set "PATH=%USERPROFILE%\.cargo\bin;%PATH%"
) else (
    echo [OK] uv already installed.
)

cd /d "%PIPELINE_ROOT%"
echo [+] Syncing dependencies and registering project...

:: Sincronizar usando modo copia
call uv sync --link-mode=copy

:: Instalar en modo editable para asegurar que src/ sea reconocido
call uv pip install -e .

:: Crear directorio bin local
set "BIN_DIR=%USERPROFILE%\.local\bin"
if not exist "%BIN_DIR%" mkdir "%BIN_DIR%"

set "ATERU_BAT=%BIN_DIR%\ateru.bat"

echo [+] Creating global bin: %ATERU_BAT%

:: --- CAMBIO AQUÍ: Ahora incluimos PIPELINE_ROOT\src en el PYTHONPATH ---
(
echo @echo off
echo set "PYTHONPATH=%PIPELINE_ROOT%\src;%%PYTHONPATH%%"
echo "%PIPELINE_ROOT%\.venv\Scripts\ateru.exe" %%*
) > "%ATERU_BAT%"

:: LA SOLUCIÓN AL ERROR: Todo el comando en una sola línea
set "SAFE_BIN=%USERPROFILE%\.local\bin"

echo [+] Updating PATH Registry...
powershell -NoProfile -Command "$p = [Environment]::GetEnvironmentVariable('Path', 'User'); if ($p -notlike '*%SAFE_BIN%*') { [Environment]::SetEnvironmentVariable('Path', $p + ';%SAFE_BIN%', 'User'); Write-Host '[OK] Added to User PATH.' -Fore Green } else { Write-Host '[!] Already in PATH.' -Fore Yellow }"

:: Refrescar la sesión actual
set "PATH=%PATH%;%SAFE_BIN%"

echo.
echo =========================================
echo    INSTALLATION DONE
echo =========================================
echo [!] Si 'ateru' no es reconocido, reinicia tu terminal.
echo [!] Intenta escribir: ateru --help
echo.
pause