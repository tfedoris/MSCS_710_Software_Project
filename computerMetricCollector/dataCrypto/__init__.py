from Cryptodome.Cipher import AES, PKCS1_OAEP
from Cryptodome.PublicKey import RSA
from Cryptodome.Random import get_random_bytes
import pandas as pd


def encrypt_data(collector, key_file):
    collector.logger.debug("Encrypting " + type(collector).__name__ + " data")
    df = collector.metrics_df
    metrics_to_encrypt = collector.metrics_to_encrypt
    public_key = RSA.import_key(open(key_file).read())
    # Store the nonce and session key to be use in decrypting data
    for idx, row in df.iterrows():
        num_bytes = 16
        session_key = get_random_bytes(num_bytes)
        cipher_rsa = PKCS1_OAEP.new(public_key)
        enc_session_key = cipher_rsa.encrypt(session_key)
        cipher_aes = AES.new(session_key, AES.MODE_EAX)
        df.loc[idx, "Nonce"] = cipher_aes.nonce
        df.loc[idx, "SessionKey"] = enc_session_key
        for col in metrics_to_encrypt:
            if col in row:
                data = str(row[col]).encode("utf-8")
                ciphertext = cipher_aes.encrypt(data)
                df.loc[idx, col] = ciphertext
    collector.metrics_df = df
    collector.logger.debug("End encrypting " + type(collector).__name__ + " data")


def decrypt_data(dataframe, col_to_decrypt, key_file):
    private_key = RSA.import_key(open(key_file).read())
    cipher_rsa = PKCS1_OAEP.new(private_key)
    for idx, row in dataframe.iterrows():
        encrypted_key = eval(row["SessionKey"])
        nonce = eval(row["Nonce"])
        session_key = cipher_rsa.decrypt(encrypted_key)
        cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
        for col in col_to_decrypt:
            cipher_text = eval(row[col])
            data = cipher_aes.decrypt(cipher_text)
            row[col] = data.decode("utf-8")
        dataframe.loc[idx] = row
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
        if not file.startswith("decrypted"):
            collector = file.split(".")[0]
            encrypted_metrics = settings["collectors"][collector]["metrics_to_encrypt"]
            encrypt_df = pd.read_csv(data_path + "\\" + file)
            decrypt_df = decrypt_data(encrypt_df, encrypted_metrics, key_file)
            decrypt_df.to_csv(data_path + "\\decrypted_" + file)
