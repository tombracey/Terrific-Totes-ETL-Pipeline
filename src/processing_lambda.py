import logging
import boto3 
import pandas as pd
import os
import json
# temporary includes:
from utils.fetch_latest_row_versions import fetch_latest_row_versions



logger = logging.getLogger("logger")
logger.setLevel(logging.INFO)


def processing_lambda_handler(event, context):
    output = event
    has_new_rows = event['HasNewRows']
    last_checked_time = event['LastCheckedTime']
    s3_client = boto3.client('s3')
    INGESTION_BUCKET_NAME = os.environ['INGESTION_BUCKET_NAME']
    PROCESSING_BUCKET_NAME = os.environ['PROCESSING_BUCKET_NAME']

    if has_new_rows['counterparty']:
        file_name = f'counterparty/{last_checked_time}.json'
        json_string = s3_client.get_object(
            Bucket=INGESTION_BUCKET_NAME, 
            Key=file_name
            )['Body'].read().decode('utf-8')
        dim_counterparty_df = pd.DataFrame.from_dict(json.loads(json_string))
        
        address_ids_to_fetch = dim_counterparty_df['legal_address_id'].tolist()
        addresses_df = fetch_latest_row_versions(s3_client, INGESTION_BUCKET_NAME, 'address', address_ids_to_fetch)
        merged_df = pd.merge(
            dim_counterparty_df, addresses_df, how='left', left_on='legal_address_id', right_on='address_id')
        pd.set_option('display.max_colwidth', None)
        print(merged_df)
    logger.info(output)
    return output


if __name__ == '__main__':
    test_event = {'HasNewRows': {'counterparty': True, 'currency': False, 'department': False, 'design': False, 'staff': False, 'sales_order': False, 'address': False, 'payment': False, 'purchase_order': False, 'payment_type': False, 'transaction': False}, 'LastCheckedTime': '2024-11-20 15:22:10.531518'}
    processing_lambda_handler(test_event, {})