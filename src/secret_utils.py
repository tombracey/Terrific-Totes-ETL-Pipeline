import json


def store_secret(sm_client, secret_id, user, password):
    secret_string = json.dumps({
        "user": user,
        "password": password
    })
    response = sm_client.create_secret(Name=secret_id, SecretString=secret_string)
    return response


def retrieve_secret(sm_client, secret_id):
    secret_json = sm_client.get_secret_value(SecretId=secret_id)['SecretString']
    secret_value = json.loads(secret_json)
    return secret_value

