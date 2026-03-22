#!/usr/bin/env bash
set -euo pipefail

echo "========================================="
echo "   Ateru Remote Installer"
echo "========================================="


OS="$(uname)"
echo "[+] Detected OS: $OS"


if ! command -v git >/dev/null 2>&1; then
    echo "[!] git not found. Installing..."
    if [[ "$OS" == "Linux" ]]; then
        if command -v apt >/dev/null 2>&1; then sudo apt update && sudo apt install -y git; fi
        if command -v dnf >/dev/null 2>&1; then sudo dnf install -y git; fi
    elif [[ "$OS" == "Darwin" ]]; then
        brew install git
    fi
fi

if ! command -v curl >/dev/null 2>&1; then
    echo "[!] curl not found. Installing..."
    if [[ "$OS" == "Linux" ]]; then
        if command -v apt >/dev/null 2>&1; then sudo apt install -y curl; fi
        if command -v dnf >/dev/null 2>&1; then sudo dnf install -y curl; fi
    elif [[ "$OS" == "Darwin" ]]; then
        brew install curl
    fi
fi


TMP_DIR="$(mktemp -d)"
echo "[+] Cloning Ateru repo into $TMP_DIR"
git clone --depth 1 https://github.com/ronnyascencio/ateru.git "$TMP_DIR"


echo "[+] Running set_up_unix.sh..."
bash "$TMP_DIR/scripts/set_up_unix.sh"


echo "[+] Cleaning up temporary files..."
rm -rf "$TMP_DIR"

echo ""
echo "========================================="
echo "   Ateru Remote Installation COMPLETE"
echo "========================================="
echo ""
echo "[IMPORTANT] Close terminal, open a new one, and run:"
echo "    ateru --help"
