@echo off
setlocal enabledelayedexpansion

echo =========================================
echo    Ateru Pipeline Setup (Windows)
echo =========================================

:: 1. Force copy mode for Dropbox compatibility
set "UV_LINK_MODE=copy"

:: 2. Get absolute path of the root (where src/ and pyproject.toml live)
:: Assuming the .bat is located in the 'scripts' folder
pushd "%~dp0.."
set "PIPELINE_ROOT=%CD%"
popd

echo [+] PIPELINE_ROOT detected: %PIPELINE_ROOT%

:: 3. Save User Environment Variables (Persistent)
setx PIPELINE_ROOT "%PIPELINE_ROOT%" > nul

:: 4. Check and Install 'uv' if missing
where uv >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [!] uv not found. Installing uv...
    powershell -NoProfile -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    set "PATH=%USERPROFILE%\.cargo\bin;%PATH%"
) else (
    echo [OK] uv is already installed.
)

:: 5. Sync virtual environment and dependencies
cd /d "%PIPELINE_ROOT%"
echo [+] Syncing virtual environment (copy mode)...
call uv sync --link-mode=copy

:: 6. Register project in editable mode
echo [+] Installing 'ateru' in editable mode...
call uv pip install -e .

:: 7. Create the global launcher (ateru.bat)
set "BIN_DIR=%USERPROFILE%\.local\bin"
if not exist "%BIN_DIR%" mkdir "%BIN_DIR%"
set "ATERU_LAUNCHER=%BIN_DIR%\ateru.bat"

echo [+] Creating global launcher at: %ATERU_LAUNCHER%

:: --- CRITICAL FIX: Ensure CWD is PIPELINE_ROOT during execution ---
(
echo @echo off
echo set "PIPELINE_ROOT=%PIPELINE_ROOT%"
echo set "PYTHONPATH=%%PIPELINE_ROOT%%\src;%%PYTHONPATH%%"
echo pushd "%%PIPELINE_ROOT%%"
echo "%%PIPELINE_ROOT%%\.venv\Scripts\python.exe" -m ateru.cli.main %%*
echo popd
) > "%ATERU_LAUNCHER%"

:: 8. Ensure the user bin directory is in the PATH
echo [+] Updating User PATH Registry...
set "SAFE_BIN=%USERPROFILE%\.local\bin"

powershell -NoProfile -Command ^
    "$p = [Environment]::GetEnvironmentVariable('Path', 'User'); ^
    if ($p -notlike '*%SAFE_BIN%*') { ^
        [Environment]::SetEnvironmentVariable('Path', $p + ';%SAFE_BIN%', 'User'); ^
        Write-Host '[OK] Added to User PATH.' -Fore Green ^
    } else { ^
        Write-Host '[!] Already in PATH.' -Fore Yellow ^
    }"

:: 9. Refresh current session path
set "PATH=%PATH%;%SAFE_BIN%"

echo.
echo =========================================
echo          INSTALLATION COMPLETE
echo =========================================
echo.
echo [IMPORTANT] To use the 'ateru' command:
echo 1. CLOSE this terminal.
echo 2. OPEN a NEW terminal window.
echo 3. Type: ateru --help
echo.
pause