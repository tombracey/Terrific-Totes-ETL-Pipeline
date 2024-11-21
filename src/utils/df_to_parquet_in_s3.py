import pandas as pd
import pyarrow
import os
# need to add following to requirements.txt:
# pandas
# pyarrow
# parquet-tools

# json_string = '[{"currency_id": 1, "currency_code": "GBP", "created_at": "2022-11-03 14:20:49.962000", "last_updated": "2022-11-03 14:20:49.962000"}, {"currency_id": 2, "currency_code": "USD", "created_at": "2022-11-03 14:20:49.962000", "last_updated": "2022-11-03 14:20:49.962000"}, {"currency_id": 3, "currency_code": "EUR", "created_at": "2022-11-03 14:20:49.962000", "last_updated": "2022-11-03 14:20:49.962000"}]'
# df = pd.read_json(json_string)
# df.to_parquet('./test_parquet', engine='auto', compression=None)

# 'parquet-tools inspect test_parquet' view parquet file



def df_to_parquet_in_s3(client, df, bucket_name, folder, file_name):
    # os.mkdir("tmp")
    df.to_parquet(f"./tmp/{file_name}.parquet") 

    client.upload_file(f"./tmp/{file_name}.parquet", bucket_name, f"{folder}/{file_name}")

    os.remove(f"./tmp/{file_name}.parquet")  