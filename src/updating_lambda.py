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
def insert_into_dw(df,db,table_name):
    column_names = ", ".join(df.columns)
    placehoders = ", ".join(["%s"] * len(df.columns))
    print(column_names)
    cursor = db.cursor() 
    insert_statement = f"""
        INSERT INTO {table_name} ({column_names})
        VALUES ({placehoders});
        """
    print(insert_statement)
    for index, row in df.iterrows():
        print(row)
        cursor.execute(insert_statement, row)
    
    db.commit()
    cursor.close()
    
   
# LAMBDA HANDLER
def updating_lambda_handler(event, context):

    BUCKET_NAME = os.environ["PROCESSING_BUCKET_NAME"]
    
    last_checked_time = event["LastCheckedTime"]
    s3_client = boto3.client("s3")
    db = connect_to_db()

    has_new_rows = event["HasNewRows"]
    
    for table_name in has_new_rows:
        if has_new_rows[table_name]:
            file_key=f"{table_name}/{last_checked_time}.parquet"
            df = read_parquet_from_s3(s3_client,BUCKET_NAME,file_key)
            insert_into_dw(df,db,table_name)
    
    close_connection(db)    