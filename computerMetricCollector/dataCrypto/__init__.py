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
    private_key = RSA.import_key(open(key_file).read())
    cipher_rsa = PKCS1_OAEP.new(private_key)
    df_by_key = dict(tuple(dataframe.groupby(["SessionKey", "Nonce"])))
    for key, nonce_str in df_by_key.keys():
        df = df_by_key[(key, nonce_str)]
        encrypted_key = eval(key)
        nonce = eval(nonce_str)
        session_key = cipher_rsa.decrypt(encrypted_key)
        cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
        for idx, row in df.iterrows():
            for col in col_to_decrypt:
                cipher_text = eval(row[col])
                data = cipher_aes.decrypt(cipher_text)
                row[col] = data.decode("utf-8")
            df.loc[idx] = row
        df_by_key[(key, nonce_str)] = df
    dataframe = pd.concat(df_by_key.values())
    return dataframe


if __name__ == "__main__":
    import os
    from computerMetricCollector import config

    data_path = "C:\\data\\xfer\\collectorLocal"
    files = os.listdir(data_path)
    settings = config.import_config("C:\\Users\\Admin\\Desktop\\CompSci\\MSCS_710\\MSCS_710_Software_Project" +
                                    "\\computerMetricCollector")
    key_file = "C:\\Users\\Admin\\Desktop\\CompSci\\MSCS_710\\MSCS_710_Software_Project\\computerMetricCollector\\dataCrypto\\ppk\\private.pem"
    for file in files:
        collector = file.split(".")[0]
        encrypted_metrics = settings["collectors"][collector]["metrics_to_encrypt"]
        encrypt_df = pd.read_csv(data_path + "\\" + file)
        decrypt_df = decrypt_data(encrypt_df, encrypted_metrics, key_file)
        print(decrypt_df)
