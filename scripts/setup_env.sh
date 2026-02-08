#!/usr/bin/env bash
set -e

echo "=== Ateru Pipeline setup ==="

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
# Create global ateru command
# --------------------------------------------------
BIN_DIR="$HOME/.local/bin"
mkdir -p "$BIN_DIR"
ATERU_BIN="$BIN_DIR/ateru"

cat <<'EOF' > "$ATERU_BIN"
#!/usr/bin/env bash
set -e

# Force PYTHONPATH to ateru/
if [ -z "$PYTHONPATH" ]; then
    export PYTHONPATH="$(cd "$(dirname "$0")/../.." && pwd)/ateru"
else
    export PYTHONPATH="$(cd "$(dirname "$0")/../.." && pwd)/ateru:$PYTHONPATH"
fi

cd "$(cd "$(dirname "$0")/../.." && pwd)"

exec uv run python ateru/cli/main.py "$@"
EOF

chmod +x "$ATERU_BIN"
echo "ateru command installed at $ATERU_BIN"

# Add to PATH
if ! echo "$PATH" | grep -q "$HOME/.local/bin"; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$SHELL_RC"
fi
