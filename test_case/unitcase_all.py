import unittest, logging
from aes_cipher.aes_cipher import AESGCMCipher

class TestAESCipher(unittest.TestCase):
    def setUp(self):
        self.password = b'my_secret_password'
        self.cipher = AESGCMCipher(self.password)

    #This test checks if the encryption and decryption work correctly together. It ensures that the decrypted text matches the original plaintext.
    def test_encrypt_decrypt(self):
        plaintext = b'Test message'
        nonce, salt, ciphertext, tag = self.cipher.encrypt(plaintext)
        result = self.cipher.decrypt(nonce, salt, ciphertext, tag)
        self.assertEqual(plaintext, result)
        logging.info(self.assertEqual(plaintext, result))

    #This test is similar to test_encrypt_decrypt but uses the batch methods. It verifies that each encrypted and then decrypted message matches the corresponding original plaintext.
    def test_batch_encrypt_decrypt(self):
        plaintexts = [b'Hello, AES-GCM!', b'Second Message', b'Third Message']
        encrypted_texts = self.cipher.batch_encrypt(plaintexts)
        decrypted_texts = self.cipher.batch_decrypt(encrypted_texts)
        for plaintext, decrypted_text in zip(plaintexts, decrypted_texts):
            self.assertEqual(plaintext, decrypted_text)

    #This test ensures that the encryption method produces a non-empty output.
    def test_encrypt_nonempty_output(self):
        plaintext = b'Test message'
        nonce, salt, ciphertext, tag = self.cipher.encrypt(plaintext)
        self.assertTrue(ciphertext)

    #This test checks the behavior when decryption is attempted with an incorrect authentication tag. It should raise a ValueError.
    def test_decrypt_with_wrong_tag(self):
        plaintext = b'Test message'
        nonce, salt, ciphertext, tag = self.cipher.encrypt(plaintext)
        wrong_tag = b'000000000000'
        with self.assertRaises(ValueError):
            self.cipher.decrypt(nonce, salt, ciphertext, wrong_tag)

if __name__ == '__main__':
    logging.info(unittest.main())
