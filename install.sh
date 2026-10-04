#!/usr/bin/env bash
set -e
DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"

python3 -m pip install --user cryptography

cat > "$DIR/206s" << EOF
#!/usr/bin/env bash
PYTHONPATH="$DIR" exec python3 -m tool.cli "\$@"
EOF
chmod +x "$DIR/206s"

ALIAS_LINE="alias 206s='$DIR/206s'"
FISH_ALIAS_LINE="alias 206s '$DIR/206s'"

add_line() {
  local file="$1"
  local line="$2"
  mkdir -p "$(dirname "$file")"
  touch "$file"
  if ! grep -Fq "$line" "$file"; then
    echo "$line" >> "$file"
    echo "[+] Alias added to $file"
  fi
}

add_line "$HOME/.bashrc" "$ALIAS_LINE"
add_line "$HOME/.zshrc" "$ALIAS_LINE"
add_line "$HOME/.config/fish/config.fish" "$FISH_ALIAS_LINE"

echo "[+] Restart your shell, then run: 206s"