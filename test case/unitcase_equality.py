import unittest
import os
from aes_cipher.aes_cipher import AESCipher

class TestAESCipher(unittest.TestCase):
    def test_encrypt_decrypt(self):
        key = os.urandom(32)
        aes = AESCipher(key)
        plaintext = b"Test AES encryption and decryption"
        
        ciphertext = aes.encrypt(plaintext)
        decrypted_text = aes.decrypt(ciphertext)

        self.assertEqual(plaintext, decrypted_text)


if __name__ == '__main__':
    unittest.main()
