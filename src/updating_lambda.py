import boto3, os, logging, json, io
from pg8000.native import Connection
import pandas as pd

logger = logging.getLogger("logger")
logger.setLevel(logging.INFO)


# RETRIEVE SECRET UTIL
def retrieve_secret(sm_client, secret_id):
    logger.info(f"retrieving secret {secret_id}")
    secret_json = sm_client.get_secret_value(SecretId=secret_id)["SecretString"]
    secret_value = json.loads(secret_json)
    return secret_value


# CONNECTION
def connect_to_db():
    sm_client = boto3.client("secretsmanager", "eu-west-2")
    credentials = retrieve_secret(sm_client, "gb-ttotes/postgres-olap-credentials")

    return Connection(
        user=credentials["DW_USER"],
        password=credentials["DW_PASSWORD"],
        database=credentials["DW_DATABASE"],
        host=credentials["DW_HOST"],
        port=credentials["DW_PORT"],
    )


def close_connection(conn):
    conn.close()

# PARQUET TO DF
def read_parquet_from_s3(s3_client,BUCKET_NAME,file_key):
    response = s3_client.get_object(
            Bucket=BUCKET_NAME, Key=file_key
        )
    buffer = io.BytesIO(response["Body"].read())
    df = pd.read_parquet(buffer)
    return df

# INSERT INTO DW
def insert_into_dw(df,db):
    insert_statement = """
        INSERT INTO dim_currency (currency_id, currency_code, currency_name)
        VALUES (1, 'two', 3);
        """
    # for row in df.itertuples(index=False, name=None):
    #     db.run(insert_statement, row)
    db.run(insert_statement)
        
    close_connection(db)
   
# LAMBDA HANDLER
def updating_lambda_handler(event, context):

    BUCKET_NAME = os.environ["PROCESSING_BUCKET_NAME"]
    
    last_checked_time = event["LastCheckedTime"]
    s3_client = boto3.client("s3")
    db = connect_to_db()

    has_new_rows = event["HasNewRows"]
    if has_new_rows["dim_currency"]:
        response = s3_client.get_object(
            Bucket=BUCKET_NAME, Key=f"dim_currency/{last_checked_time}.parquet"
        )
        buffer = io.BytesIO(response["Body"].read())
        df = pd.read_parquet(buffer)
        
        insert_statement = """
        INSERT INTO dim_currency (currency_id, currency_code, currency_name)
        VALUES (%s, %s, %s)
        """
        for row in df.itertuples(index=False, name=None):
            db.run(insert_statement, row)

    close_connection(db)    