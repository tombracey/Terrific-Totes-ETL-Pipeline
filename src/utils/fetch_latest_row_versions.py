import json
import pandas as pd

def fetch_latest_row_versions(s3_client, bucket_name, table_name, list_of_ids):
    id_col_name = f"{table_name}_id"

    # look in folder of S3 bucket
    file_list = s3_client.list_objects(
        Bucket=bucket_name,
        Prefix=f"{table_name}/"
    )['Contents']

    latest_row_dicts = []

    for i in range(len(file_list), 0, -1):
        cur_filename = file_list[i-1]['Key']

        json_object = s3_client.get_object(
            Bucket=bucket_name,
            Key=cur_filename
        )
        json_string = json_object['Body'].read().decode("utf-8")

        row_dicts = json.loads(json_string)
        for j in range(len(row_dicts), 0, -1):
            if row_dicts[j-1][id_col_name] in list_of_ids:
                latest_row_dicts.append(row_dicts[j-1])
                list_of_ids.remove(row_dicts[j-1][id_col_name])

    return pd.DataFrame(latest_row_dicts)

