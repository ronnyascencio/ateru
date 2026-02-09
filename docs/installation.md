# Installation Guide

Currently, Xolo Pipeline officially supports **Linux**.

## Prerequisites

- Python 3.11+
- `curl` (for the automated installer)
- `uv` (will be installed automatically if using the installer)

## Automated Installation (Recommended)

The repository includes an installer script that handles environment variables, `uv` installation, and CLI aliasing.

Linux:

```bash
git clone [https://github.com/ronnyascencio/ateru](https://github.com/ronnyascencio/ateru.git)
cd ateru
chmod +x scripts/setup_env.sh
./scripts/setup_env.sh
```

Windows:

```bash
git clone [https://github.com/ronnyascencio/ateru](https://github.com/ronnyascencio/ateru.git)
cd ateru
./scripts/set_up_windows.bat
```

![installation](docs/media/demo.gif)

## Alternative: Manual with `uv`

If you prefer to manage environments manually:

1. Create and sync the virtual environment:

```bash
uv sync
```

2. Register environment variables:

```bash
on linux:

source scripts/setup_env.sh

on windows:
scripts/set_up_windows.bat

```

> This sets `PIPELINE_ROOT`, `SYSTEM_ROOT`, and modifies your shell rc so Xolo tools work as expected.

Restart your terminal so the new environment variables and PATH changes take effect.

3. Verify the installation with:

```bash
ateru --help
```
