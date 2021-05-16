import mysql.connector
import json
import collections
from Cryptodome.Cipher import AES, PKCS1_OAEP
from Cryptodome.PublicKey import RSA
from Cryptodome.Random import get_random_bytes
from datetime import date, datetime
import pandas as pd
import os


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if isinstance(obj, bytearray):
        return obj.decode()
    raise TypeError("Type %s not serializable" % type(obj))


print('Loading function')

# Configuration Values fr warproject
endpoint = os.environ['ENDPOINT']
username = os.environ['USERNAME']
password = os.environ['PASSWORD']
database_name = os.environ['PRIMARY_DB_NAME']

# Configuration Values for waruserinfo
user_info_database_name = os.environ['SECONDARY_DB_NAME']

# Connection
connection = mysql.connector.connect(
    host=endpoint, user=username, password=password, database=database_name, auth_plugin='mysql_native_password')


def lambda_handler(event, context):
    query = "SELECT * from " + event["table_name"]

    dataframe = pd.read_sql(query, connection, parse_dates=["entry_time"])

    pkey = '''-----BEGIN PRIVATE KEY-----
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
5PHziuP2xUVETeRoFUHmw3AD1DuTX3xV
-----END PRIVATE KEY-----'''

    dataframe = decrypt_data(dataframe, pkey)

    response_object = {}
    response_object['success'] = True
    response_object['headers'] = {}
    response_object['headers']['X-Requested-With'] = '*'
    response_object['headers']['Access-Control-Allow-Headers'] = 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,x-requested-with'
    response_object['headers']['Access-Control-Allow-Origin'] = '*'
    response_object['headers']['Access-Control-Allow-Methods'] = 'POST,OPTIONS'
    response_object['data'] = dataframe.to_json(
        orient="records", date_format="iso")

    return response_object


def decrypt_data(dataframe, key):
    private_key = RSA.importKey(key)
    cipher_rsa = PKCS1_OAEP.new(private_key)
    for idx, row in dataframe.iterrows():
        encrypted_key = bytes.fromhex(row["session_key"].decode())
        nonce = bytes.fromhex(row["nonce"].decode())
        session_key = cipher_rsa.decrypt(encrypted_key)
        cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
        for col, val in row.items():
            if not isinstance(val, bytearray) or col in ("nonce", "session_key"):
                continue
            cipher_text = bytes.fromhex(val.decode())
            data = cipher_aes.decrypt(cipher_text)
            row[col] = data.decode("utf-8")
        dataframe.loc[idx] = row
    return dataframe
