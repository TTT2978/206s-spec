import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

DEFAULT_ITER = 390000


def derive_key(password, salt, iterations):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
    )
    return kdf.derive(password.encode("utf-8"))


def encrypt(plaintext, password, iterations, aad):
    salt = os.urandom(16)
    nonce = os.urandom(12)
    key = derive_key(password, salt, iterations)
    ciphertext = AESGCM(key).encrypt(nonce, plaintext, aad)
    return salt, nonce, ciphertext


def decrypt(salt, nonce, ciphertext, password, iterations, aad):
    key = derive_key(password, salt, iterations)
    return AESGCM(key).decrypt(nonce, ciphertext, aad)