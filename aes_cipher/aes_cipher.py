from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os, logging

class AESCipher:
    def __init__(self, key):
        self.key = key

    def encrypt(self, plaintext):
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(self.key), modes.CFB(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext) + encryptor.finalize()
        return iv + ciphertext

    def decrypt(self, ciphertext):
        iv = ciphertext[:16]
        cipher = Cipher(algorithms.AES(self.key), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        return decryptor.update(ciphertext[16:]) + decryptor.finalize()


class AESGCMCipher:
    def __init__(self, password):
        self.password = password

    def generate_key(self, salt):
        # Use PBKDF2 for key derivation
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        return kdf.derive(self.password)

    def encrypt(self, plaintext):
        # Generate a random salt
        salt = os.urandom(16)
        key = self.generate_key(salt)
        # Generate a random nonce
        nonce = os.urandom(12)
        algorithm = algorithms.AES(key)
        mode = modes.GCM(nonce)
        cipher = Cipher(algorithm, mode, backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext) + encryptor.finalize()
        return nonce, salt, ciphertext, encryptor.tag

    def decrypt(self, nonce, salt, ciphertext, tag):
        key = self.generate_key(salt)
        algorithm = algorithms.AES(key)
        mode = modes.GCM(nonce, tag)
        cipher = Cipher(algorithm, mode, backend=default_backend())
        decryptor = cipher.decryptor()
        return decryptor.update(ciphertext) + decryptor.finalize()

    def batch_encrypt(self, plaintexts):
        return [self.encrypt(plaintext) for plaintext in plaintexts]

    def batch_decrypt(self, encrypted_data):
        return [self.decrypt(nonce, salt, ciphertext, tag) for nonce, salt, ciphertext, tag in encrypted_data]