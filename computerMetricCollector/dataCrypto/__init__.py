from Cryptodome.Cipher import AES, PKCS1_OAEP
from Cryptodome.PublicKey import RSA
from Cryptodome.Random import get_random_bytes
import pandas as pd


def encrypt_data(collector, key_file):
    df = collector.metrics_df
    metrics_to_encrypt = collector.metrics_to_encrypt
    public_key = RSA.import_key(open(key_file).read())
    session_key = get_random_bytes(16)
    cipher_rsa = PKCS1_OAEP.new(public_key)
    enc_session_key = cipher_rsa.encrypt(session_key)
    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    df = df.assign(Nonce=cipher_aes.nonce)
    df = df.assign(SessionKey=enc_session_key)
    for idx, row in df.iterrows():
        row = row.copy()
        for col in metrics_to_encrypt:
            data = str(row[col]).encode("utf-8")
            ciphertext = cipher_aes.encrypt(data)
            df.loc[idx, col] = ciphertext
    collector.metrics_df = df


def decrypt_data(dataframe, col_to_decrypt, key_file):
    decrypt_df = pd.DataFrame(columns=dataframe.columns)
    private_key = RSA.import_key(open(key_file).read())
    for row in dataframe.iterrows():
        encrypted_key = row["Session_key"]
        nonce = row["Nonce"]
        cipher_rsa = PKCS1_OAEP.new(private_key)
        session_key = cipher_rsa.decrypt(encrypted_key)
        cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
        for col in col_to_decrypt:
            cipher_text = row[col]
            data = cipher_aes.decrypt(cipher_text)
            row[col] = data
        decrypt_df.append(row)
    return decrypt_df
