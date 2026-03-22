#!/usr/bin/env bash
set -euo pipefail

echo "========================================="
echo "   Ateru Remote Installer"
echo "========================================="


OS="$(uname)"
echo "[+] Detected OS: $OS"


for cmd in git curl; do
    if ! command -v $cmd >/dev/null 2>&1; then
        echo "[!] $cmd not found. Installing..."
        if [[ "$OS" == "Linux" ]]; then
            if command -v apt >/dev/null 2>&1; then sudo apt update && sudo apt install -y $cmd; fi
            if command -v dnf >/dev/null 2>&1; then sudo dnf install -y $cmd; fi
        elif [[ "$OS" == "Darwin" ]]; then
            brew install $cmd
        fi
    fi
done

DEFAULT_DIR="$HOME/pipeline"

echo ""
read -p "Enter installation directory [default: $DEFAULT_DIR]: " INSTALL_DIR


INSTALL_DIR="${INSTALL_DIR:-$DEFAULT_DIR}"


mkdir -p "$INSTALL_DIR"

echo "[+] Ateru will be installed in: $INSTALL_DIR"


if [ -d "$INSTALL_DIR/ateru" ]; then
    echo "[!] Directory $INSTALL_DIR/ateru already exists."
    read -p "Do you want to overwrite it? [y/N]: " OVERWRITE
    if [[ "$OVERWRITE" =~ ^[Yy]$ ]]; then
        rm -rf "$INSTALL_DIR/ateru"
    else
        echo "Installation cancelled."
        exit 1
    fi
fi

echo "[+] Cloning Ateru repo..."
git clone --depth 1 https://github.com/ronnyascencio/ateru.git "$INSTALL_DIR/ateru"


echo "[+] Running set_up_unix.sh..."
bash "$INSTALL_DIR/ateru/scripts/set_up_unix.sh"

echo ""
echo "========================================="
echo "   Ateru Remote Installation COMPLETE"
echo "========================================="
echo ""
echo "[IMPORTANT] Close terminal, open a new one, and run:"
echo "    ateru --help"