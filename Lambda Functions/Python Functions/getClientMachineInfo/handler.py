import mysql.connector
import json
import collections
from Cryptodome.Cipher import AES, PKCS1_OAEP
from Cryptodome.PublicKey import RSA
from Cryptodome.Random import get_random_bytes
from datetime import date, datetime
import pandas as pd
import os
import requests


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
username = os.environ['USER_NAME']
password = os.environ['PASSWORD']
database_name = os.environ['PRIMARY_DB_NAME']

# Configuration Values for waruserinfo
user_info_database_name = os.environ['SECONDARY_DB_NAME']

api_url = "https://ytp3g6j58c.execute-api.us-east-2.amazonaws.com/test/get-private-key"

# Connection
connection = mysql.connector.connect(
    host=endpoint, user=username, password=password, database=database_name, auth_plugin='mysql_native_password')


def lambda_handler(event, context):
    post_obj = {"registration_id": event["registration_id"]}
    api_response = requests.post(api_url, json=post_obj)
    response_data = api_response.json()

    pkey = response_data["data"]["private_key"]
    user_id = response_data["data"]["user_id"]

    query = "\
    SELECT A.*\
    FROM " + event["table_name"] + " AS A\
    INNER JOIN map_user_machine AS B\
    ON B.machine_id = A.machine_id\
    WHERE user_id=\"" + user_id + "\""

    dataframe = pd.read_sql(query, connection, parse_dates=["entry_time"])

    print(dataframe.to_json(
        orient="records", date_format="iso"))

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
            print(col)
            print(val.decode())
            cipher_text = bytes.fromhex(val.decode())
            data = cipher_aes.decrypt(cipher_text)
            row[col] = data.decode("utf-8")
        dataframe.loc[idx] = row
    return dataframe
