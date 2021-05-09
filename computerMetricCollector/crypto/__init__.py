from Cryptodome.Cipher import AES, PKCS1_OAEP
from Cryptodome.PublicKey import RSA
from Cryptodome.Random import get_random_bytes
import requests
import pandas as pd


def generate_rsa_ppk(private_file_path, public_file_path):
    bits = 2048
    key = RSA.generate(bits)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    with open(private_file_path, "bw+") as private_file:
        private_file.seek(0)
        private_file.write(private_key)
        private_file.truncate()
        private_file.close()
    with open(public_file_path, "bw+") as public_file:
        public_file.seek(0)
        public_file.write(public_key)
        public_file.close()


def get_key(reg_id, url):
    response = requests.post(url, data={"registrationId": reg_id})
    res_json = response.json()
    public_key = None
    if res_json.get("success") and res_json.get("data"):
        data = res_json.get("data")
        public_key = data.get("publicKey")
    return public_key


def encrypt_data(collector, key):
    collector.logger.debug("Encrypting " + type(collector).__name__ + " data")
    df = collector.metrics_df
    metrics_to_encrypt = collector.metrics_to_encrypt
    public_key = RSA.import_key(key)
    cipher_rsa = PKCS1_OAEP.new(public_key)
    num_bytes = 16
    # Store the nonce and session key to be use in decrypting data
    for idx, row in df.iterrows():
        session_key = get_random_bytes(num_bytes)
        enc_session_key = cipher_rsa.encrypt(session_key)
        cipher_aes = AES.new(session_key, AES.MODE_EAX)
        df.loc[idx, "Nonce"] = cipher_aes.nonce.hex()
        df.loc[idx, "SessionKey"] = enc_session_key.hex()
        for col in metrics_to_encrypt:
            if col in row:
                data = str(row[col]).encode("utf-8")
                ciphertext = cipher_aes.encrypt(data)
                df.loc[idx, col] = ciphertext.hex()
    collector.metrics_df = df
    collector.logger.debug("End encrypting " + type(collector).__name__ + " data")


def decrypt_data(dataframe, col_to_decrypt, key):
    private_key = RSA.import_key(key)
    cipher_rsa = PKCS1_OAEP.new(private_key)
    for idx, row in dataframe.iterrows():
        encrypted_key = bytes.fromhex(row["SessionKey"])
        nonce = bytes.fromhex(row["Nonce"])
        session_key = cipher_rsa.decrypt(encrypted_key)
        cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
        for col in col_to_decrypt:
            cipher_text = bytes.fromhex(str(row[col]))
            data = cipher_aes.decrypt(cipher_text)
            row[col] = data.decode("utf-8")
        dataframe.loc[idx] = row
    return dataframe


if __name__ == "__main__":
    import os
    from computerMetricCollector.config import import_config
    root_dir = os.path.dirname(os.path.dirname(__file__))
    settings = import_config(root_dir)
    data_path = root_dir + settings.get("local_store_dir")
    files = os.listdir(data_path)
    key_file = root_dir + settings.get("encryption_key_file")
    for file in files:
        if not file.startswith("decrypted"):
            collector = file.split(".")[0]
            encrypted_metrics = settings["collectors"][collector]["metrics_to_encrypt"]
            columns = settings["collectors"][collector]["metrics"]
            csv_path = data_path + "\\" + file
            encrypt_df = pd.read_csv(csv_path, names=columns, dtype=str)
            decrypt_key = open(key_file).read()
            decrypt_df = decrypt_data(encrypt_df, encrypted_metrics, decrypt_key)
            csv_path = data_path + "\\decrypted_" + file
            if os.path.exists(csv_path):
                decrypt_df.to_csv(csv_path, mode="a", header=False, index=False, index_label=False)
            else:
                decrypt_df.to_csv(csv_path, header=False, index=False, index_label=False)
