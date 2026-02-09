#!/usr/bin/env bash
set -e

echo "=== Ateru Pipeline setup (Linux/macOS) ==="

# Obtener la raíz del proyecto (un nivel arriba de donde está este script)
PIPELINE_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export PIPELINE_ROOT
echo "PIPELINE_ROOT set to: $PIPELINE_ROOT"

SYSTEM_ROOT="/"
export SYSTEM_ROOT
echo "SYSTEM_ROOT set to: $SYSTEM_ROOT"

# --------------------------------------------------
# uv install
# --------------------------------------------------
if ! command -v uv >/dev/null 2>&1; then
    echo "uv not found. Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source $HOME/.cargo/env
else
    echo "uv already installed"
fi

# --------------------------------------------------
# Sync dependencies
# --------------------------------------------------
cd "$PIPELINE_ROOT"
echo "[+] Syncing dependencies..."
uv sync


uv pip install -e .

# --------------------------------------------------
# Create global ateru command
# --------------------------------------------------
BIN_DIR="$HOME/.local/bin"
mkdir -p "$BIN_DIR"
ATERU_BIN="$BIN_DIR/ateru"

echo "[+] Creating wrapper at $ATERU_BIN"


cat <<EOF > "$ATERU_BIN"
#!/usr/bin/env bash

# PYTHONPATH apunta a la carpeta src para encontrar el paquete ateru
export PYTHONPATH="$PIPELINE_ROOT/src:\$PYTHONPATH"
export PIPELINE_ROOT="$PIPELINE_ROOT"

# Ejecutamos el punto de entrada definido en pyproject.toml
exec "$PIPELINE_ROOT/.venv/bin/ateru" "\$@"
EOF

chmod +x "$ATERU_BIN"

# --------------------------------------------------
# Add to PATH (Detectar el shell correcto)
# --------------------------------------------------
SHELL_RC=""
case "$SHELL" in
    */zsh)  SHELL_RC="$HOME/.zshrc" ;;
    */bash) SHELL_RC="$HOME/.bashrc" ;;
    *)      SHELL_RC="$HOME/.profile" ;;
esac

if ! echo "$PATH" | grep -q "$BIN_DIR"; then
    echo "Adding $BIN_DIR to PATH in $SHELL_RC"
    echo "export PATH=\"$BIN_DIR:\$PATH\"" >> "$SHELL_RC"
    echo "[!] Please run: source $SHELL_RC"
fi

echo "========================================="
echo "   INSTALLATION DONE"
echo "========================================="