# Installation Guide

Currently, Xolo Pipeline officially supports **Linux**.

## Prerequisites
* Python 3.11+
* `curl` (for the automated installer)
* `uv` (will be installed automatically if using the installer)

## Automated Installation (Recommended)
The repository includes an installer script that handles environment variables, `uv` installation, and CLI aliasing.

```bash
git clone [https://gitlab.com/xololab/xolo-pipeline.git](https://gitlab.com/xololab/xolo-pipeline.git)
cd xolo-pipeline
chmod +x scripts/setup_env.sh
./scripts/setup_env.sh
```


## Alternative: Manual with `uv`

If you prefer to manage environments manually:

1. Create and sync the virtual environment:

```bash
uv venv
uv sync
```

2. Register environment variables:

```bash
source scripts/setup_env.sh
```

> This sets `PIPELINE_ROOT`, `SYSTEM_ROOT`, and modifies your shell rc so Xolo tools work as expected.

Restart your terminal (or run `source ~/.bashrc` / `source ~/.zshrc`) so the new environment variables and PATH changes take effect.

3. Verify the installation with:

```bash
xolo --help
```
