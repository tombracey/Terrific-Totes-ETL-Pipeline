from src.utils.fetch_latest_row_versions import fetch_latest_row_versions
import pytest, os, boto3
import pandas as pd
from moto import mock_aws

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


@pytest.fixture
def s3_bucket(s3_client):
    s3_client.create_bucket(Bucket="test_bucket")
    yield s3_client


@mock_aws
def test_empty_bucket_returns_empty_dataframe():
    pass


@mock_aws
def test_single_file_with_correct_id_returns_expect_single_row_dataframe(s3_bucket):
    s3_bucket.upload_file(
        Bucket="test_bucket",
        Filename="test/test_data/sales_order/2024-11-21 13_32_38.364280.json",
        Key="sales_order/2024-11-21 13_32_38.364280.json"
    )
    output_df = fetch_latest_row_versions("sales_order", [11283])
    assert isinstance(output_df, pd.DataFrame)
    assert len(output_df.index) == 1
    assert output_df.loc[0, "sales_order_id"] == 11283
    assert type(output_df.loc[0, "created_at"]) == timestamp ## .dtype()?