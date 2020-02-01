import os, sys

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

backend = default_backend()


def func_sha256(msg):
    digest = hashes.Hash(hashes.SHA256(), backend=backend)
    digest.update(msg)
    return digest.finalize()


def derive_pbkdf2hmac(msg, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=backend,
    )
    key = kdf.derive(msg)
    return key


def enc_aesgcm(key, msg, auth):
    cipher = AESGCM(key)
    nonce = os.urandom(16)
    ciphertext = cipher.encrypt(nonce, msg, auth)
    return (ciphertext, nonce)


def dec_aesgcm(key, auth, nonce, ct):
    cipher = AESGCM(key)
    text = cipher.decrypt(nonce, ct, auth)
    return text


def test_crypt():
    password = b"12345"
    message = b"This is a test message"
    salt = os.urandom(16)

    secret = derive_pbkdf2hmac(password, salt)
    key = secret
    print("New secret key >> ", key)

    hashed_secret = func_sha256(key)
    print("New Hash >> ", hashed_secret)

    encrypted = enc_aesgcm(key, message, password)
    nonce = encrypted[1]
    ciphertext = encrypted[0]
    print("Encrypted message >> ", ciphertext)
    print("Ciphertext size: ", len(ciphertext))

    plaintext = dec_aesgcm(key, password, nonce, ciphertext)
    print("Decrypted message >> ", plaintext)

