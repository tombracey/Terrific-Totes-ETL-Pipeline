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
        user=credentials["PG_USER"],
        password=credentials["PG_PASSWORD"],
        database=credentials["PG_DATABASE"],
        host=credentials["PG_HOST"],
        port=credentials["PG_PORT"],
    )

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
        