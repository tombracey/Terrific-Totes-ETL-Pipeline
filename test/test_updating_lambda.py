from src.updating_lambda import*
from pg8000.native import Connection
import pg8000
from moto import mock_aws
import pytest, boto3, os
from src.utils.df_to_parquet_in_s3 import df_to_parquet_in_s3


def connect_to_db():
    sm_client = boto3.client("secretsmanager", "eu-west-2")
    credentials = retrieve_secret(sm_client, "gb-ttotes/test-db-credentials")


    return pg8000.connect(
        user=credentials["TEST_USER"],
        password=credentials["TEST_PASSWORD"],
        database=credentials["TEST_DB"],
        host=credentials["TEST_HOST"],
        port=credentials["TEST_PORT"],
        )

@mock_aws
def test_util_read_parquet_from_s3():
    s3_client = boto3.client('s3')
    s3_client.create_bucket(Bucket="processing-test-bucket",
                            CreateBucketConfiguration={"LocationConstraint":"eu-west-2"})
    test_json = '[{"currency_id": 1, "currency_code": "GBP", "currency_name": "British pound sterling"}]'
    test_df = pd.read_json(test_json)
    test_folder = "test-folder"
    test_file_name = "test-file-name"
    df_to_parquet_in_s3(s3_client, test_df, "processing-test-bucket", test_folder, test_file_name)
    output = read_parquet_from_s3(s3_client,"processing-test-bucket",f"{test_folder}/{test_file_name}.parquet")
    # print(output)
    assert isinstance(output,pd.DataFrame)
    

def test_util_insert_row_into_data_warehouse():
    
    test_dict = {"currency_id": [1], "currency_code": ["GBP"], "currency_name": ["British pound sterling"]}
    test_df = pd.DataFrame(test_dict)
    db = connect_to_db()
    db.run("DROP TABLE IF EXISTS dim_currency;")
    db.run("CREATE TABLE IF NOT EXISTS dim_currency (currency_id INT, currency_code VARCHAR, currency_name VARCHAR);")
    insert_into_dw(test_df,db,"dim_currency")
    assert db.run("SELECT * FROM dim_currency;") == ([1, 'GBP', 'British pound sterling'],)
    db.close()

def test_util_insert_multiple_rows_into_data_warehouse():
    
    test_dict = {"currency_id": [1,2], "currency_code": ["GBP","USD"], "currency_name": ["British pound sterling","US dollar"]}
    test_df = pd.DataFrame(test_dict)
    db = connect_to_db()
    db.run("DROP TABLE IF EXISTS dim_currency;")
    db.run("CREATE TABLE IF NOT EXISTS dim_currency (currency_id INT, currency_code VARCHAR, currency_name VARCHAR);")
    insert_into_dw(test_df,db,"dim_currency")
    assert db.run("SELECT * FROM dim_currency;") == ([1, 'GBP', 'British pound sterling'],[2, "USD", "US dollar"])
    db.close()