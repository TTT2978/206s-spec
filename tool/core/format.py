import secrets
import string
import struct

from tool.core import container
from tool.core import manifest

MAIN_NAME = "main.bin"
ALPHABET = string.ascii_letters + string.digits
NAME_LEN = 16
SALT_LEN = 16
NONCE_LEN = 12


def random_name(used):
    while True:
        name = "".join(secrets.choice(ALPHABET) for _ in range(NAME_LEN)) + ".bin"
        if name not in used:
            return name


def make_aad(iterations):
    return struct.pack(">BBHI", manifest.VERSION, manifest.SUITE, 0, iterations)


def pack(outer_text, salt, nonce, ciphertext, iterations):
    text_name = random_name({MAIN_NAME})
    hidden_name = random_name({MAIN_NAME, text_name})
    main = manifest.build(text_name, hidden_name, iterations)
    entries = [
        (MAIN_NAME, main),
        (text_name, outer_text.encode("utf-8")),
        (hidden_name, salt + nonce + ciphertext),
    ]
    secrets.SystemRandom().shuffle(entries)
    return container.pack(entries)


def load(data):
    try:
        entries = container.unpack(data)
        info = manifest.parse(entries[MAIN_NAME])
        text = entries[info["text_name"]]
        hidden = entries[info["hidden_name"]]
        if len(hidden) < SALT_LEN + NONCE_LEN:
            raise ValueError("corrupted hidden layer")
        return {
            "created": info["created"],
            "iterations": info["iterations"],
            "text": text,
            "salt": hidden[:SALT_LEN],
            "nonce": hidden[SALT_LEN:SALT_LEN + NONCE_LEN],
            "ciphertext": hidden[SALT_LEN + NONCE_LEN:],
            "aad": make_aad(info["iterations"]),
        }
    except Exception:
        raise ValueError("invalid 206s file")