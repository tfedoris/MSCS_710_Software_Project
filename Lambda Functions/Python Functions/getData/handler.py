import mysql.connector
import json
import collections
from Cryptodome.Cipher import AES, PKCS1_OAEP
from Cryptodome.PublicKey import RSA
from Cryptodome.Random import get_random_bytes
from datetime import date, datetime


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if isinstance(obj, bytearray):
        return obj.decode()
    raise TypeError("Type %s not serializable" % type(obj))


print('Loading function')

# Configuration Values fr warproject
endpoint = 'wardatabase.cm9i2tottiif.us-west-2.rds.amazonaws.com'
username = 'admin'
password = '12345678'
database_name = 'warproject'

# Configuration Values for waruserinfo
user_info_endpoint = 'wardatabase.cm9i2tottiif.us-west-2.rds.amazonaws.com'
user_info_username = 'admin'
user_info_password = '12345678'
user_info_database_name = 'waruserinfo'

# Connection
connection = mysql.connector.connect(
    host=endpoint, user=username, password=password, database=database_name, auth_plugin='mysql_native_password')


def lambda_handler(event, context):
    cursor = connection.cursor()
    cursor.execute('SELECT * from client_machine')

    row_headers = [x[0] for x in cursor.description]

    rows = cursor.fetchall()

    json_data = []

    for row in rows:
        json_data.append(dict(zip(row_headers, row)))

    json_data = decrypt_data(json_data, "-----BEGIN PRIVATE KEY-----\n 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\n 1cnMVHS+5l1qf/afmMbRlx")

    response_object = {}
    response_object['success'] = True
    response_object['headers'] = {}
    response_object['headers']['X-Requested-With'] = '*'
    response_object['headers']['Access-Control-Allow-Headers'] = 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,x-requested-with'
    response_object['headers']['Access-Control-Allow-Origin'] = '*'
    response_object['headers']['Access-Control-Allow-Methods'] = 'POST,OPTIONS'
    response_object['data'] = json.dumps(json_data, default=json_serial)

    return response_object


def decrypt_data(rows, key):
    private_key = key
    cipher_rsa = PKCS1_OAEP.new(private_key)
    for idx, row in enumerate(rows):
        encrypted_key = row["session_key"]
        nonce = row["nounce"]
        session_key = cipher_rsa.decrypt(encrypted_key)
        cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
        for col in row[idx]:
            if not isinstance(col, bytearray):
                continue
            cipher_text = row[col]
            data = cipher_aes.decrypt(cipher_text)
            row[col] = data.decode()
        rows[idx] = row
    return rows
