#!/usr/bin/env bash
set -e

echo "=== Xolo Pipeline setup ==="

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
    export PATH="$HOME/.cargo/bin:$PATH"
else
    echo "uv already installed"
fi

# --------------------------------------------------
# Sync dependencies
# --------------------------------------------------
cd "$PIPELINE_ROOT"
uv sync

# --------------------------------------------------
# Create global xolo command
# --------------------------------------------------
BIN_DIR="$HOME/.local/bin"
mkdir -p "$BIN_DIR"
XOLO_BIN="$BIN_DIR/xolo"

cat <<'EOF' > "$XOLO_BIN"
#!/usr/bin/env bash
set -e

# Force PYTHONPATH to xolo/
if [ -z "$PYTHONPATH" ]; then
    export PYTHONPATH="$(cd "$(dirname "$0")/../.." && pwd)/xolo"
else
    export PYTHONPATH="$(cd "$(dirname "$0")/../.." && pwd)/xolo:$PYTHONPATH"
fi

cd "$(cd "$(dirname "$0")/../.." && pwd)"

exec uv run python xolo/cli/xolo_cli/main.py "$@"
EOF

chmod +x "$XOLO_BIN"
echo "xolo command installed at $XOLO_BIN"

# Add to PATH
if ! echo "$PATH" | grep -q "$HOME/.local/bin"; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$SHELL_RC"
fi
