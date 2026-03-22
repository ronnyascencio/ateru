#!/usr/bin/env bash
set -euo pipefail

echo "========================================="
echo "   Ateru Pipeline Setup (Unix)"
echo "========================================="
echo ""

# --------------------------------------------------
# 1. Force copy mode (igual que Windows)
# --------------------------------------------------
export UV_LINK_MODE=copy

# --------------------------------------------------
# 2. Detect PIPELINE_ROOT (igual que %~dp0..)
# --------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PIPELINE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

export PIPELINE_ROOT

echo "[+] PIPELINE_ROOT detected: $PIPELINE_ROOT"

# --------------------------------------------------
# 3. Persist environment variable (equivalente a setx)
# --------------------------------------------------
case "$SHELL" in
    */zsh)  SHELL_RC="$HOME/.zshrc" ;;
    */bash) SHELL_RC="$HOME/.bashrc" ;;
    *)      SHELL_RC="$HOME/.profile" ;;
esac

if ! grep -q "PIPELINE_ROOT=" "$SHELL_RC" 2>/dev/null; then
    echo "[+] Saving PIPELINE_ROOT in $SHELL_RC"
    echo "export PIPELINE_ROOT=\"$PIPELINE_ROOT\"" >> "$SHELL_RC"
fi

# --------------------------------------------------
# 4. Check / install uv
# --------------------------------------------------
if ! command -v uv >/dev/null 2>&1; then
    echo "[!] uv not found. Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source "$HOME/.cargo/env"
else
    echo "[OK] uv is already installed"
fi

# --------------------------------------------------
# 5. Sync environment
# --------------------------------------------------
cd "$PIPELINE_ROOT"

echo "[+] Syncing virtual environment (copy mode)..."
uv sync --link-mode=copy

# --------------------------------------------------
# 6. Install editable
# --------------------------------------------------
echo "[+] Installing 'ateru' in editable mode..."
uv pip install -e .

# --------------------------------------------------
# 7. Create global launcher (equivalente al .bat)
# --------------------------------------------------
BIN_DIR="$HOME/.local/bin"
mkdir -p "$BIN_DIR"

ATERU_BIN="$BIN_DIR/ateru"

echo "[+] Creating global launcher at: $ATERU_BIN"

cat > "$ATERU_BIN" <<EOF
#!/usr/bin/env bash

export PIPELINE_ROOT="$PIPELINE_ROOT"
export PYTHONPATH="\$PIPELINE_ROOT/src:\$PYTHONPATH"

cd "\$PIPELINE_ROOT"
exec "\$PIPELINE_ROOT/.venv/bin/python" -m ateru.cli.main "\$@"
EOF

chmod +x "$ATERU_BIN"

# --------------------------------------------------
# 8. Add to PATH (persistente)
# --------------------------------------------------
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo "[+] Adding $BIN_DIR to PATH in $SHELL_RC"
    echo "export PATH=\"$BIN_DIR:\$PATH\"" >> "$SHELL_RC"
    echo "[!] Run: source $SHELL_RC"
fi

# --------------------------------------------------
# 9. Refresh PATH (sesión actual)
# --------------------------------------------------
export PATH="$PATH:$BIN_DIR"

# --------------------------------------------------
# DONE
# --------------------------------------------------
echo ""
echo "========================================="
echo "        INSTALLATION COMPLETE"
echo "========================================="
echo ""
echo "[IMPORTANT]"
echo "1. CLOSE this terminal"
echo "2. OPEN a new terminal"
echo "3. Run: ateru --help"
echo ""
