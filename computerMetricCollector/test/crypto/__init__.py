from Cryptodome.Cipher import PKCS1_OAEP, AES
from Cryptodome.PublicKey import RSA


def read_key(keyFile):
    with open(keyFile) as f:
        key = f.read()
    return key

def decrypt_data(dataframe, col_to_decrypt, key):
    private_key = RSA.import_key(key)
    cipher_rsa = PKCS1_OAEP.new(private_key)
    for idx, row in dataframe.iterrows():
        encrypted_key = bytes.fromhex(row["session_key"])
        nonce = bytes.fromhex(row["nonce"])
        session_key = cipher_rsa.decrypt(encrypted_key)
        cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
        for col in col_to_decrypt:
            cipher_text = bytes.fromhex(str(row[col]))
            data = cipher_aes.decrypt(cipher_text)
            row[col] = data.decode("utf-8")
        dataframe.loc[idx] = row
    return dataframe
