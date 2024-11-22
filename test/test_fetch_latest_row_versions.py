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
    s3_client.create_bucket(
        Bucket="test_bucket",
        CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
    )
    yield s3_client


def test_single_file_with_correct_id_returns_expected_single_row_dataframe(s3_bucket):
    s3_bucket.upload_file(
        Bucket="test_bucket",
        Filename="test/test_data/sales_order/2024-11-21 13_32_38.364280.json",
        Key="sales_order/2024-11-21 13_32_38.364280.json",
    )
    output_df = fetch_latest_row_versions(
        s3_bucket, "test_bucket", "sales_order", [11283]
    )
    assert isinstance(output_df, pd.DataFrame)
    assert len(output_df.index) == 1
    assert output_df.loc[0, "sales_order_id"] == 11283
    assert output_df.loc[0, "created_at"] == "2024-11-21 13:21:09.941000"
    assert output_df.loc[0, "last_updated"] == "2024-11-21 13:21:09.941000"
    assert output_df.loc[0, "design_id"] == 349
    assert output_df.loc[0, "staff_id"] == 1
    assert output_df.loc[0, "counterparty_id"] == 5
    assert output_df.loc[0, "units_sold"] == 1842
    assert output_df.loc[0, "unit_price"] == 2.29
    assert output_df.loc[0, "currency_id"] == 2
    assert output_df.loc[0, "agreed_delivery_date"] == "2024-11-26"
    assert output_df.loc[0, "agreed_payment_date"] == "2024-11-25"
    assert output_df.loc[0, "agreed_delivery_location_id"] == 15


def test_seeking_one_id_in_multiple_matching_files_returns_expected_single_row_dataframe(
    s3_bucket,
):
    s3_bucket.upload_file(
        Bucket="test_bucket",
        Filename="test/test_data/sales_order/2024-11-21 15_47_38.454675.json",
        Key="sales_order/2024-11-21 15_47_38.454675.json",
    )
    s3_bucket.upload_file(
        Bucket="test_bucket",
        Filename="test/test_data/sales_order/2024-11-21 13_32_38.364280.json",
        Key="sales_order/2024-11-21 13_32_38.364280.json",
    )
    s3_bucket.upload_file(
        Bucket="test_bucket",
        Filename="test/test_data/sales_order/2024-11-21 16_02_38.340563.json",
        Key="sales_order/2024-11-21 16_02_38.340563.json",
    )

    output_df = fetch_latest_row_versions(
        s3_bucket, "test_bucket", "sales_order", [11283]
    )

    assert len(output_df.index) == 1
    assert output_df.loc[0, "sales_order_id"] == 11283
    assert output_df.loc[0, "created_at"] == "2024-11-21 15:54:09.995000"
    assert output_df.loc[0, "last_updated"] == "2024-11-21 15:54:09.995000"
    assert output_df.loc[0, "design_id"] == 78
    assert output_df.loc[0, "staff_id"] == 8
    assert output_df.loc[0, "counterparty_id"] == 18
    assert output_df.loc[0, "units_sold"] == 53443
    assert output_df.loc[0, "unit_price"] == 2.54
    assert output_df.loc[0, "currency_id"] == 2
    assert output_df.loc[0, "agreed_delivery_date"] == "2024-11-22"
    assert output_df.loc[0, "agreed_payment_date"] == "2024-11-25"
    assert output_df.loc[0, "agreed_delivery_location_id"] == 8


def test_seeking_multiple_ids_in_multiple_files_returns_expected_dataframe(s3_bucket):
    s3_bucket.upload_file(
        Bucket="test_bucket",
        Filename="test/test_data/sales_order/2024-11-21 15_47_38.454675.json",
        Key="sales_order/2024-11-21 15_47_38.454675.json",
    )
    s3_bucket.upload_file(
        Bucket="test_bucket",
        Filename="test/test_data/sales_order/2024-11-21 13_32_38.364280.json",
        Key="sales_order/2024-11-21 13_32_38.364280.json",
    )
    s3_bucket.upload_file(
        Bucket="test_bucket",
        Filename="test/test_data/sales_order/2024-11-21 16_02_38.340563.json",
        Key="sales_order/2024-11-21 16_02_38.340563.json",
    )

    output_df = fetch_latest_row_versions(
        s3_bucket, "test_bucket", "sales_order", [11283, 11285, 11291]
    )

    assert len(output_df.index) == 3

    index_1 = output_df.query("sales_order_id == 11283").index[0]
    last_updated_1 = output_df.query("sales_order_id == 11283").loc[
        index_1, "last_updated"
    ]
    assert last_updated_1 == "2024-11-21 15:54:09.995000"

    index_2 = output_df.query("sales_order_id == 11285").index[0]
    last_updated_2 = output_df.query("sales_order_id == 11285").loc[
        index_2, "last_updated"
    ]
    assert last_updated_2 == "2024-11-21 13:32:09.809000"

    index_3 = output_df.query("sales_order_id == 11291").index[0]
    last_updated_3 = output_df.query("sales_order_id == 11291").loc[
        index_3, "last_updated"
    ]
    assert last_updated_3 == "2024-11-21 15:40:10.078000"
