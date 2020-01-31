import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def func_sha256(msg, backend):
    digest = hashes.Hash(hashes.SHA256(), backend=backend)
    digest.update(msg)
    return digest.finalize()

def func_pbkdf2hmac(msg, backend):
    salt = os.urandom(16)

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=backend
    )
    key = kdf.derive(msg)
    return (key, salt)

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
    backend = default_backend()
    password = b'12345'
    message = b'This is a test message'

    secret = func_pbkdf2hmac(password, backend)
    key = secret[0]
    salt = secret[1]
    print('New secret key >> ', key)

    hashed_secret = func_sha256(key, backend)
    print('New Hash >> ', hashed_secret)

    encrypted = enc_aesgcm(key, message, password)
    nonce = encrypted[1]
    ciphertext = encrypted[0]
    print('Encrypted message >> ', ciphertext)

    plaintext = dec_aesgcm(key, password, nonce, ciphertext)
    print('Decrypted message >> ', plaintext)

