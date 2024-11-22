import pandas as pd
import pyarrow
import os
# need to add following to requirements.txt:
# pandas
# pyarrow

def df_to_parquet_in_s3(client, df, bucket_name, folder, file_name):
    # os.mkdir("tmp")
    df.to_parquet(f"./tmp/{file_name}.parquet") 

    client.upload_file(f"./tmp/{file_name}.parquet", bucket_name, f"{folder}/{file_name}.parquet")

    os.remove(f"./tmp/{file_name}.parquet")  