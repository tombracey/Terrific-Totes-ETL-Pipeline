import json
import datetime
import boto3
import os
import pg8000.native
from dotenv import load_dotenv





# RETRIEVE SECRET UTIL

def retrieve_secret(sm_client, secret_id):
    secret_json = sm_client.get_secret_value(SecretId=secret_id)["SecretString"]
    secret_value = json.loads(secret_json)
    return secret_value

# UPDATE SECRET

def update_secret(sm_client, secret_id, keys_and_values):
    if isinstance(keys_and_values[0], list):
        key_value_dict = {}
        for key_value_pair in keys_and_values:
            key_value_dict[key_value_pair[0]] = key_value_pair[1]
    else:
        key_value_dict = {keys_and_values[0]: keys_and_values[1]}
    
    secret_string = json.dumps(key_value_dict)
    response = sm_client.update_secret(SecretId=secret_id, SecretString=secret_string)
    return response



"""
TABLES TO INGEST
counterparty
currency
department
design
staff
sales_order
address
payment
purchase_order
payment_type
transaction
"""
# GET DATA

def get_data(db, last_update):

    data = {}

    tables = ['counterparty', 'currency', 'department', 'design', 'staff', 'sales_order', 'address', 'payment', 'purchase_order', 'payment_type', 'transaction']

    for table in tables:

        query = db.run(f"SELECT * FROM {table} WHERE last_updated >= :last_update;", last_update=last_update)
        data[table] = (query, [col["name"] for col in db.columns])



    # counterparty = db.run(
    #     "SELECT * FROM counterparty WHERE last_updated >= :last_update;",
    #     last_update=last_update,
    # )
    # data["counterparty"] = (counterparty, [col["name"] for col in db.columns])

    # currency = db.run(
    #     "SELECT * FROM currency WHERE last_updated >= :last_update;",
    #     last_update=last_update,
    # )
    # data["currency"] = (currency, [col["name"] for col in db.columns])

    # department = db.run(
    #     "SELECT * FROM department WHERE last_updated >= :last_update;",
    #     last_update=last_update,
    # )
    # data["department"] = (department, [col["name"] for col in db.columns])

    # design = db.run(
    #     "SELECT * FROM design WHERE last_updated >= :last_update;",
    #     last_update=last_update,
    # )
    # data["design"] = (design, [col["name"] for col in db.columns])

    # staff = db.run(
    #     "SELECT * FROM staff WHERE last_updated >= :last_update;",
    #     last_update=last_update,
    # )
    # data["staff"] = (staff, [col["name"] for col in db.columns])

    # sales_order = db.run(
    #     "SELECT * FROM sales_order WHERE last_updated >= :last_update;",
    #     last_update=last_update,
    # )
    # data["sales_order"] = (sales_order, [col["name"] for col in db.columns])

    # address = db.run(
    #     "SELECT * FROM address WHERE last_updated >= :last_update;",
    #     last_update=last_update,
    # )
    # data["address"] = (address, [col["name"] for col in db.columns])

    # payment = db.run(
    #     "SELECT * FROM payment WHERE last_updated >= :last_update;",
    #     last_update=last_update,
    # )
    # data["payment"] = (payment, [col["name"] for col in db.columns])

    # purchase_order = db.run(
    #     "SELECT * FROM purchase_order WHERE last_updated >= :last_update;",
    #     last_update=last_update,
    # )
    # data["purchase_order"] = (purchase_order, [col["name"] for col in db.columns])

    # payment_type = db.run(
    #     "SELECT * FROM payment_type WHERE last_updated >= :last_update;",
    #     last_update=last_update,
    # )
    # data["payment_type"] = (payment_type, [col["name"] for col in db.columns])

    # transaction = db.run(
    #     "SELECT * FROM transaction WHERE last_updated >= :last_update;",
    #     last_update=last_update,
    # )
    # data["transaction"] = (transaction, [col["name"] for col in db.columns])

    return data

# DATE TO STRFTIME

def datetime_to_strftime(row):
    new_row = row.copy()
    for i in range(len(row)):
        if isinstance(row[i], datetime.datetime):
            new_item = row[i].strftime("%Y-%m-%d %H:%M:%S.%f")
            new_row[i] = new_item
    return new_row

# ZIP DICTIONARY

def zip_dictionary(new_rows, columns):
    
    zipped_dict = [dict(zip(columns, row)) for row in new_rows]
    
    return zipped_dict

# FORMAT TO JSON

def format_to_json(list_of_dicts):
    formatted_data = json.dumps(list_of_dicts)
    return formatted_data

# JSON TO s3
def json_to_s3(client, json_string, bucket_name, folder, file_name):

    with open(f"{os.getcwd()}/{file_name}", "w", encoding="UTF-8") as file:
        file.write(json_string)

    client.upload_file(
        f"{os.getcwd()}/{file_name}", bucket_name, f"{folder}/{file_name}"
    )

    os.remove(f"{os.getcwd()}/{file_name}")
# CONNECTION
def connect_to_db():
    sm_client = boto3.client("secretsmanager", "eu-west-2")
    credentials = retrieve_secret(sm_client, "gb-ttotes/totesys-oltp-credentials")

    return pg8000.native.Connection(
        user=credentials["PG_USER"],
        password=credentials["PG_PASSWORD"],
        database=credentials["PG_DATABASE"],
        host=credentials["PG_HOST"],
        port=credentials["PG_PORT"],
    )

# STORE SECRET (create)
def store_secret(sm_client, secret_id, keys_and_values):

    if isinstance(keys_and_values[0], list):
        key_value_dict = {}
        for key_value_pair in keys_and_values:
            key_value_dict[key_value_pair[0]] = key_value_pair[1]
    else:
        key_value_dict = {keys_and_values[0]: keys_and_values[1]}

    secret_string = json.dumps(key_value_dict)
    response = sm_client.create_secret(Name=secret_id, SecretString=secret_string)
    return response

# LAMBDA HANDLER
def ingestion_lambda_handler():
    db = connect_to_db()
    sm_client = boto3.client('secretsmanager')
    secret_request = sm_client.list_secrets()
    list_of_secrets = secret_request['SecretList']
    secret_names = [secret['Name'] for secret in list_of_secrets]
    
    if 'last_update' not in secret_names:
        date_and_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        last_update = (datetime.datetime(2020, 1, 1, 00, 00, 00, 000000)).strftime(
        "%Y-%m-%d %H:%M:%S.%f")
        store_secret(sm_client, 'last_update', ['last_update', date_and_time])
    else:
        last_updated_secret = retrieve_secret(sm_client, 'last_update')
        last_update = last_updated_secret['last_update']
        date_and_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        update_secret(sm_client, 'last_update', ['last_update', date_and_time])
    
    data = get_data(db, last_update)
    
    for table in data:
        rows = data[table][0]
        columns = data[table][1]
        new_rows = []
        for row in rows:
            new_rows.append(datetime_to_strftime(row))
        zipped_dict = zip_dictionary(new_rows, columns)
        json_data = format_to_json(zipped_dict)
        file_name = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        folder_name = table
        s3_client = boto3.client('s3')
        json_to_s3(s3_client, json_data, "green-bean-ingestion-bucket", folder_name, file_name)

