import pandas as pd
from deprecated.crypto import decrypt_data

'''
Run this program to decrypt encrypted data
'''
if __name__ == "__main__":
    import os
    from computerMetricCollector.config import import_config
    root_dir = os.path.dirname(os.path.dirname(__file__))
    settings = import_config(root_dir)
    data_path = root_dir + settings.get("local_store_dir")
    files = os.listdir(data_path)
    key_file = root_dir + "/crypto/ppk/private.pem"
    for file in files:
        if not file.startswith("decrypted") and file.endswith(".csv"):
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