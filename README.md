# 206s — Private Container Format

A command-line tool that hides and encrypts sensitive text inside a single `.206s` file. The outer text is readable, but the hidden content requires a password.

## Features

- **AES-256-GCM encryption** — military-grade encryption for hidden content
- **Single file** — outer text and hidden data packed into one `.206s` archive
- **No visible traces** — examining the file doesn't reveal the hidden layer
- **Three operations**: Make (create), Read (view plain text), Decoder (decrypt with password)
- **Flexible output** — display on terminal or export to `.txt` file
- **Cross-platform** — works on Linux, macOS, Android (Termux), Windows

## Installation

### Linux / macOS / Termux (Bash, Zsh, Fish)

```bash
cd 206s_tool
./install.sh
```

Then restart your shell and run:

```bash
206s
```

### Windows (PowerShell)

```powershell
cd 206s_tool
powershell -File install.ps1
```

Then restart PowerShell and run:

```powershell
206s
```

## Usage

Run `206s` from any directory. You'll see a menu:

```
[+] Select mode:

  > Make
    Read
    Decoder
```

Use arrow keys to select and Enter to confirm.

### Make — Create a .206s file

1. Enter a filename (e.g., `secret.206s`)
2. Edit outer text in nano (what anyone can see)
3. Edit hidden text in nano (encrypted, password-protected)
4. Enter a password
5. File saved as `secret.206s`

### Read — View the outer text (no password needed)

1. Enter the `.206s` filename
2. Choose: Show here or Export to .txt

### Decoder — View the hidden text (password required)

1. Enter the `.206s` filename
2. Enter the password
3. Choose: Show here or Export to .txt

## Example

```bash
$ 206s
[+] Select mode:
  > Make
    Read
    Decoder
```

Pick Make → filename `note.206s` → add outer text "Hello" → add hidden text "Secret message" → password `mypass123` → done.

Later, to read the outer text:

```bash
$ 206s
# Pick Read → note.206s → Show here or Export
```

To read the hidden text:

```bash
$ 206s
# Pick Decoder → note.206s → password: mypass123 → Show here or Export
```

## Requirements

- Python 3.7+
- `cryptography` library (installed automatically)
- `nano` text editor (usually pre-installed on Linux/macOS/Termux)

## CLI Only

This tool runs **only on command line**. No GUI, no web interface.

## License

Open source. Use at your own risk.
