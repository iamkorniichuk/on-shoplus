from base64 import b64decode, b64encode
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5


class Rsa:
    def __init__(self, public_key):
        decoded_key = b64decode(public_key)
        self.key = RSA.import_key(decoded_key)

    def encrypt(self, data):
        cipher = PKCS1_v1_5.new(self.key)
        encrypted_data = cipher.encrypt(data.encode())
        encoded_result = b64encode(encrypted_data)
        return encoded_result.decode()
