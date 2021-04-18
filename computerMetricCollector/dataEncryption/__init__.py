from base64 import b64encode

from Cryptodome.Cipher import AES, PKCS1_v1_5
from Cryptodome.PublicKey import RSA
from Cryptodome.Random import get_random_bytes


def encrypt_data(df, key_file):
    public_key = RSA.import_key(open(key_file).read())
    cipher_aes = AES.new(public_key, AES.MODE_CTR)
    for col in df.columns:
        df[col] = df[col].apply(lambda x: encrypt(x, cipher_aes))


def encrypt(data, cipher_aes):
    ciphertext = cipher_aes.decrypt(data)
    nonce = b64encode(cipher_aes.nonce).decode('utf-8')
    ct = b64encode(ct_bytes).decode('utf-8')
    for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext):

