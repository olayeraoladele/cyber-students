from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
#import os
#import time
key = "theprykey"
key_bytes = bytes(key, "utf-8")
print("Key: " + key)
#def encrypt_decrypt(var1):
def my_encrypt(OlayeraVar):

     
    aes_cipher = Cipher(algorithms.AES(key_bytes),modes.CBC(),backend=default_backend())

    aes_encryptor = aes_cipher.encryptor()
    #aes_decryptor = aes_cipher.decryptor()

    plaintext = OlayeraVar
    plaintext_bytes = bytes(plaintext, "utf-8")
    

    ciphertext_bytes = aes_encryptor.update(plaintext_bytes) + aes_encryptor.finalize()
    ciphertext = ciphertext_bytes.hex()
    return ciphertext
    


def myDecrypt(ciphertext_bytes):
     
    aes_cipher = Cipher(algorithms.AES(key_bytes),modes.CBC(),backend=default_backend())
    aes_decryptor = aes_cipher.decryptor()
    plaintext_bytes_2 = aes_decryptor.update(ciphertext_bytes) + aes_decryptor.finalize()
    plaintext_2 = str(plaintext_bytes_2, "utf-8")
    return plaintext_2
   



def hash_pass(Olay):
    # No need for timing or random messages.
    #message = os.urandom(50)
    #before = time.perf_counter()
    digest_sha256 = hashes.Hash(hashes.SHA256())
    digest_sha256.update(Olay)
    hash_sha256 = digest_sha256.finalize()
    return hash_sha256.hex()
    #after = time.perf_counter()
   ####print("SHA256: " + hash_sha256.hex())



