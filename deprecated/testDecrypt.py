import pandas as pd
import os
from computerMetricCollector.crypto import decrypt_data

if __name__ == "__main__":
    files = os.listdir("C:\\data\\xfer\\collectorLocal")
    key_file = "C:\\\Users\\\Admin\\\Desktop\\CompSci\\MSCS_710\\MSCS_710_Software_Project\\computerMetricCollector" \
               "\\dataCrypto\\ppk\\private.pem"
    dfs = []
    for file in files:
        encrypt_df = pd.read_csv(file)
        decrypt_data(encrypt_df, key_file)