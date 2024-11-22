from src.utils.df_to_parquet_in_s3 import df_to_parquet_in_s3
from moto import mock_aws
import pytest, os, boto3, pyarrow, io
import pandas as pd


@pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS Credentials for moto"""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"


@pytest.fixture
def s3_client(aws_credentials):
    with mock_aws():
        s3 = boto3.client("s3")
        yield s3


def test_df_to_parquet_and_uploads_to_s3(s3_client):
    s3_client.create_bucket(
        Bucket="test-bucket",
        CreateBucketConfiguration={
            "LocationConstraint": os.environ["AWS_DEFAULT_REGION"]
        },
    )
    test_json = '[{"currency_id": 1, "currency_code": "GBP", "created_at": "2022-11-03 14:20:49.962000", "last_updated": "2022-11-03 14:20:49.962000"}, {"currency_id": 2, "currency_code": "USD", "created_at": "2022-11-03 14:20:49.962000", "last_updated": "2022-11-03 14:20:49.962000"}, {"currency_id": 3, "currency_code": "EUR", "created_at": "2022-11-03 14:20:49.962000", "last_updated": "2022-11-03 14:20:49.962000"}]'
    
    test_df = pd.read_json(test_json)
    test_folder = "test-folder"
    test_file_name = "test-file-name"
    df_to_parquet_in_s3(s3_client, test_df,'test-bucket', test_folder, test_file_name)
    object = s3_client.list_objects(Bucket="test-bucket")

    assert object["Contents"][0]["Key"] == f"{test_folder}/{test_file_name}.parquet"

    response = s3_client.get_object(
        Bucket="test-bucket", Key=f"{test_folder}/{test_file_name}.parquet"
    )

    buff = io.BytesIO(response['Body'].read())
    df = pd.read_parquet(buff)
    assert isinstance(df, pd.DataFrame)









