import logging
import boto3 
import pandas as pd
import os
import json
from babel.numbers import get_currency_name

# temporary includes:
from src.utils.fetch_latest_row_versions import fetch_latest_row_versions


logger = logging.getLogger("logger")
logger.setLevel(logging.INFO)


def make_exclusion_list(s3_client, bucket_name, table_name, last_checked_time):
    json_object = s3_client.get_object(
        Bucket=bucket_name,
        Key=f"{table_name}/{last_checked_time}.json"
    )
    json_string = json_object['Body'].read().decode("utf-8")

    updated_rows = json.loads(json_string)

    return [row[f"{table_name}_id"] for row in updated_rows]




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
        counterparty_df = pd.DataFrame.from_dict(json.loads(json_string))
        
        address_ids_to_fetch = counterparty_df['legal_address_id'].tolist()
        addresses_df = fetch_latest_row_versions(s3_client, INGESTION_BUCKET_NAME, 'address', address_ids_to_fetch)
        dim_counterparty_df = pd.merge(
            counterparty_df, addresses_df, how='left',
            left_on='legal_address_id', right_on='address_id')
        dim_counterparty_df = dim_counterparty_df.drop(columns=[
            'legal_address_id', 
            'commercial_contact', 
            'delivery_contact',
            'created_at_x', 
            'last_updated_x', 
            'address_id', 
            'created_at_y', 
            'last_updated_y'])
        dim_counterparty_df = dim_counterparty_df.rename(columns={
            'address_line_1': 'counterparty_legal_address_line_1',
            'address_line_2': 'counterparty_legal_address_line_2',
            'district': 'counterparty_legal_district',
            'city': 'counterparty_legal_city', 
            'postal_code': 'counterparty_legal_postal_code',
            'country': 'counterparty_legal_country',
            'phone': 'counterparty_legal_phone_number'
        })
        # Save to parquet file here

    if has_new_rows['currency']:
        file_name = f'currency/{last_checked_time}.json'
        json_string = s3_client.get_object(
            Bucket=INGESTION_BUCKET_NAME, 
            Key=file_name
            )['Body'].read().decode('utf-8')
        currency_df = pd.DataFrame.from_dict(json.loads(json_string))
        dim_currency_df = currency_df.drop(columns=['last_updated',
                                                     'created_at'])
        
        dim_currency_df['currency_name'] = dim_currency_df['currency_code'].apply(get_currency_name)
        # Save to parquet file here
    
    if has_new_rows['design']:
        file_name = f'design/{last_checked_time}.json'
        json_string = s3_client.get_object(
            Bucket=INGESTION_BUCKET_NAME, 
            Key=file_name
            )['Body'].read().decode('utf-8')
        design_df = pd.DataFrame.from_dict(json.loads(json_string))
        dim_design_df = design_df.drop(columns=['last_updated',
                                                     'created_at'])
        
        # Save to parquet file here
    
    if has_new_rows['staff']:
        file_name = f'staff/{last_checked_time}.json'
        json_string = s3_client.get_object(
            Bucket=INGESTION_BUCKET_NAME, 
            Key=file_name
            )['Body'].read().decode('utf-8')
        staff_df = pd.DataFrame.from_dict(json.loads(json_string))

        department_ids_to_fetch = staff_df['department_id'].tolist()
        departments_df = fetch_latest_row_versions(
            s3_client, INGESTION_BUCKET_NAME,
            'department', department_ids_to_fetch)
        dim_staff_df = pd.merge(
            staff_df, departments_df,
            how='left', on='department_id')
        dim_staff_df = dim_staff_df.drop(columns=[
            'department_id', 
            'created_at_x', 
            'last_updated_x', 
            'manager', 
            'created_at_y', 
            'last_updated_y'])
        dim_staff_df = dim_staff_df[[
            "staff_id",
            "first_name",
            "last_name",
            "department_name",
            "location",
            "email_address"
        ]]
        dim_staff_df['location'] = dim_staff_df['location'].fillna("Undefined")

        # Save to parquet file here

    if has_new_rows['department']:
        pass

    # if has_new_rows['address']:
    #     file_name = f'address/{last_checked_time}.json'
    #     json_string = s3_client.get_object(
    #         Bucket=INGESTION_BUCKET_NAME, 
    #         Key=file_name
    #         )['Body'].read().decode('utf-8')
    #     address_df = pd.DataFrame.from_dict(json.loads(json_string))        



    logger.info(output)
    return output


if __name__ == '__main__':
    test_event = {
        'HasNewRows': {
            'counterparty': False, 
            'currency': False, 
            'department': False, 
            'design': False, 
            'staff': True, 
            'sales_order': False, 
            'address': False, 
            'payment': False, 
            'purchase_order': False, 
            'payment_type': False, 
            'transaction': False}, 
        'LastCheckedTime': '2024-11-20 15:22:10.531518'}
    processing_lambda_handler(test_event, {})