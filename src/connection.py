import pg8000.native
import os, boto3
from dotenv import load_dotenv
from src.secret_utils import retrieve_secret

load_dotenv(override=True)


def connect_to_db():
    sm_client = boto3.client("secretsmanager")
    credentials = retrieve_secret(sm_client, "gb-ttotes/totesys-oltp-credentials")

    return pg8000.native.Connection(
        user=credentials["PG_USER"],
        password=credentials["PG_PASSWORD"],
        database=credentials["PG_DATABASE"],
        host=credentials["PG_HOST"],
        port=credentials["PG_PORT"],
    )


def close_connection(conn):
    conn.close()
