#!/usr/bin/env bash
set -e

echo "=== Xolo Pipeline setup ==="

# --------------------------------------------------
# Detect shell rc file
# --------------------------------------------------
if [ -n "$ZSH_VERSION" ]; then
    SHELL_RC="$HOME/.zshrc"
else
    SHELL_RC="$HOME/.bashrc"
fi

# --------------------------------------------------
# PIPELINE_ROOT
# --------------------------------------------------
PIPELINE_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export PIPELINE_ROOT
echo "PIPELINE_ROOT set to: $PIPELINE_ROOT"

# --------------------------------------------------
# SYSTEM_ROOT
# --------------------------------------------------
case "$OSTYPE" in
  msys*|cygwin*|win32*)
    SYSTEM_ROOT="$(cmd.exe /c echo %SystemDrive% | tr -d '\r')/"
    ;;
  *)
    SYSTEM_ROOT="/"
    ;;
esac

export SYSTEM_ROOT
echo "SYSTEM_ROOT set to: $SYSTEM_ROOT"

# --------------------------------------------------
# Persist env vars
# --------------------------------------------------
if ! grep -q 'PIPELINE_ROOT=' "$SHELL_RC" 2>/dev/null; then
    echo "export PIPELINE_ROOT=$PIPELINE_ROOT" >> "$SHELL_RC"
    echo "Added PIPELINE_ROOT to $SHELL_RC"
fi

if ! grep -q 'SYSTEM_ROOT=' "$SHELL_RC" 2>/dev/null; then
    echo "export SYSTEM_ROOT=$SYSTEM_ROOT" >> "$SHELL_RC"
    echo "Added SYSTEM_ROOT to $SHELL_RC"
fi

# --------------------------------------------------
# Install uv if needed
# --------------------------------------------------
if ! command -v uv >/dev/null 2>&1; then
    echo "uv not found. Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
else
    echo "uv already installed"
fi

# --------------------------------------------------
# Sync dependencies
# --------------------------------------------------
cd "$PIPELINE_ROOT"
echo "Running uv sync..."
uv sync

# --------------------------------------------------
# Create global xolo command (uv run wrapper)
# --------------------------------------------------
BIN_DIR="$HOME/.local/bin"
mkdir -p "$BIN_DIR"

XOLO_BIN="$BIN_DIR/xolo"

cat <<'EOF' > "$XOLO_BIN"
#!/usr/bin/env bash
set -e

# --------------------------------------------------
# Detect PIPELINE_ROOT dynamically
# --------------------------------------------------
if [ -n "$PIPELINE_ROOT" ]; then
    ROOT="$PIPELINE_ROOT"
else
    # If PIPELINE_ROOT not set, guess relative to this script
    SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
    ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
fi

CLI_FILE="$ROOT/cli/xolo_cli/main.py"

cd "$ROOT"

if [ ! -f "$CLI_FILE" ]; then
    echo "Xolo CLI not found:"
    echo "$CLI_FILE"
    exit 1
fi

# Run CLI using uv to handle virtualenv and dependencies
exec uv run python "$CLI_FILE" "$@"
EOF

chmod +x "$XOLO_BIN"
echo "xolo command installed at $XOLO_BIN"

# --------------------------------------------------
# Ensure ~/.local/bin in PATH
# --------------------------------------------------
if ! echo "$PATH" | grep -q "$HOME/.local/bin"; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$SHELL_RC"
    echo "Added ~/.local/bin to PATH in $SHELL_RC"
fi

echo ""
echo "=== Installation complete ==="
echo "Restart your terminal or run:"
echo "  source $SHELL_RC"
echo ""
echo "Then try:"
echo "  xolo --help"
echo "  xolo launch blender demo"
