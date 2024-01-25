from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

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

# Example usage
if __name__ == "__main__":
    cipher = AESGCMCipher(b'my_secret_password')

    # Batch Encrypting
    plaintexts = [b'Hello, AES-GCM!', b'Second Message', b'Third Message']
    plaintext = b'Saikesh Forever'
    encrypted_texts = cipher.batch_encrypt(plaintexts)
    print("Encrypted:", encrypted_texts)

    encrypted_text = cipher.encrypt(plaintext)
    print("Encrypted-String:", encrypted_text)

    # Batch Decrypting
    decrypted_texts = cipher.batch_decrypt(encrypted_texts)
    print("Decrypted:", decrypted_texts)

    nonce, salt, ciphertext, tag = encrypted_text  # Unpacking the tuple
    decrypted_text = cipher.decrypt(nonce, salt, ciphertext, tag)  # Pass the unpacked values
    print("Decrypted-String:", decrypted_text)
