import os
import getpass

from tool.core import format as fmt
from tool.core import crypto
from tool.ui.menu import menu
from tool.ui.editor import edit_with_nano


def unique_path(path):
    if not os.path.exists(path):
        return path
    base, ext = os.path.splitext(path)
    i = 1
    while os.path.exists(f"{base}_{i}{ext}"):
        i += 1
    return f"{base}_{i}{ext}"


def ask_file():
    print("[+] Enter file path:")
    fname = input("[+] ").strip()
    if not os.path.isfile(fname) and os.path.isfile(fname + ".206s"):
        fname += ".206s"
    if not os.path.isfile(fname):
        print("[-] File not found")
        return None, None
    with open(fname, "rb") as f:
        data = f.read()
    try:
        info = fmt.load(data)
    except ValueError:
        print("[-] Invalid 206s file")
        return None, None
    return fname, info


def deliver(content, fname, suffix):
    choice = menu(["Show here", "Export to .txt"])
    if choice == "Show here":
        print("[+] Content:\n")
        print(content.decode("utf-8", errors="replace"))
        return
    out = unique_path(os.path.splitext(fname)[0] + suffix)
    with open(out, "wb") as f:
        f.write(content)
    print(f"[+] Saved: {out}")


def do_make():
    print("[+] Enter output filename:")
    fname = input("[+] ").strip()
    if not fname.endswith(".206s"):
        fname += ".206s"
    outer = edit_with_nano("[+] Opening outer layer editor...")
    inner = edit_with_nano("[+] Opening hidden layer editor...")
    password = getpass.getpass("[+] Enter password for hidden layer: ")
    iterations = crypto.DEFAULT_ITER
    aad = fmt.make_aad(iterations)
    salt, nonce, ciphertext = crypto.encrypt(inner.encode("utf-8"), password, iterations, aad)
    data = fmt.pack(outer, salt, nonce, ciphertext, iterations)
    with open(fname, "wb") as f:
        f.write(data)
    print(f"[+] File saved: {fname}")


def do_read():
    fname, info = ask_file()
    if info is None:
        return
    deliver(info["text"], fname, ".txt")


def do_decode():
    fname, info = ask_file()
    if info is None:
        return
    password = getpass.getpass("[+] Enter password: ")
    try:
        inner = crypto.decrypt(
            info["salt"], info["nonce"], info["ciphertext"],
            password, info["iterations"], info["aad"],
        )
    except Exception:
        print("[-] Invalid password or corrupted data")
        return
    deliver(inner, fname, ".hidden.txt")


def main():
    choice = menu(["Make", "Read", "Decoder"])
    if choice == "Make":
        do_make()
    elif choice == "Read":
        do_read()
    else:
        do_decode()


if __name__ == "__main__":
    main()