#!/usr/bin/env bash
#  PIPELINE_ROOT
PIPELINE_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"
export PIPELINE_ROOT
echo "PIPELINE_ROOT set to: $PIPELINE_ROOT"

# adding PATH temporal
export PATH="$PIPELINE_ROOT/cli/xolo_cli:$PATH"


# SYSTEM_ROOT
if [[ "$OSTYPE" == "msys"* || "$OSTYPE" == "cygwin"* || "$OSTYPE" == "win32"* ]]; then
    # Windows Git Bash / Cygwin
    SYSTEM_ROOT=$(cmd.exe /c "echo %SystemDrive%\" | tr -d '\r'")
else
    # Linux / macOS
    SYSTEM_ROOT="/"
fi
export SYSTEM_ROOT
echo "SYSTEM_ROOT set to: $SYSTEM_ROOT"




# make it permanent  ~/.bashrc if not exist
if ! grep -q "PIPELINE_ROOT" ~/.bashrc; then
    echo "export PIPELINE_ROOT=$PIPELINE_ROOT" >> ~/.bashrc
    echo "Added PIPELINE_ROOT permanently to ~/.bashrc"

fi

if ! grep -q "SYSTEM_ROOT" ~/.bashrc; then
    echo "export SYSTEM_ROOT=$SYSTEM_ROOT" >> ~/.bashrc
    echo "Added SYSTEM_ROOT permanently to ~/.bashrc"
fi
