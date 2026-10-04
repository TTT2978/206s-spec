import sys
import os


def getch():
    if os.name == "nt":
        import msvcrt
        ch = msvcrt.getch()
        if ch in (b"\xe0", b"\x00"):
            ch2 = msvcrt.getch()
            if ch2 == b"H":
                return "UP"
            if ch2 == b"P":
                return "DOWN"
            return None
        if ch in (b"\r", b"\n"):
            return "ENTER"
        return None
    else:
        import tty
        import termios
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
            if ch == "\x1b":
                ch2 = sys.stdin.read(1)
                ch3 = sys.stdin.read(1)
                if ch2 == "[" and ch3 == "A":
                    return "UP"
                if ch2 == "[" and ch3 == "B":
                    return "DOWN"
                return None
            if ch in ("\r", "\n"):
                return "ENTER"
            return None
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)


def menu(options):
    idx = 0
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("[+] Select mode:\n")
        for i, opt in enumerate(options):
            if i == idx:
                print(f"  > {opt}")
            else:
                print(f"    {opt}")
        key = getch()
        if key == "UP":
            idx = (idx - 1) % len(options)
        elif key == "DOWN":
            idx = (idx + 1) % len(options)
        elif key == "ENTER":
            return options[idx]