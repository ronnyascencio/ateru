#!/usr/bin/env bash
PIPELINE_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"
export PIPELINE_ROOT
echo "PIPELINE_ROOT set to: $PIPELINE_ROOT"

# adding PATH temporal
export PATH="$PIPELINE_ROOT/cli/xolo_cli:$PATH"

# make it permanent  ~/.bashrc if not exist
if ! grep -q "PIPELINE_ROOT" ~/.bashrc; then
    echo "export PIPELINE_ROOT=$PIPELINE_ROOT" >> ~/.bashrc
    echo 'export PATH="$PIPELINE_ROOT/cli:$PATH"' >> ~/.bashrc
    echo "Added PIPELINE_ROOT permanently to ~/.bashrc"
fi
