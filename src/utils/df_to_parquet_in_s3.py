import pandas as pd
import pyarrow
import os
import logging

logger = logging.getLogger("logger")
logger.setLevel(logging.INFO)

def df_to_parquet_in_s3(client, df, bucket_name, folder, file_name):
    if not os.path.exists("tmp"):
        os.mkdir("tmp")
    df.to_parquet(f"./tmp/{file_name}.parquet") 

    client.upload_file(f"./tmp/{file_name}.parquet", bucket_name, f"{folder}/{file_name}.parquet")
    logger.info(f'{folder}/{file_name}.parquet uploaded to processing')

    os.remove(f"./tmp/{file_name}.parquet")