from src.secret_utils import store_secret, retrieve_secret
import pytest, boto3
from moto import mock_aws

sm_client = boto3.client('secretsmanager')


@mock_aws
def test_secrets_are_stored_successfully():
    store_secret(sm_client, "my_secret", "keen_green_bean_1", "pa55word")
    list_secrets = sm_client.list_secrets()
    assert list_secrets['SecretList'][0]['Name'] == "my_secret"

    store_secret(sm_client, "our_secret", "keen_green_bean_2", "pa55word")
    store_secret(sm_client, "your_secret", "keen_green_bean_3", "pa55word")
    list_secrets = sm_client.list_secrets()
    assert len(list_secrets['SecretList']) == 3
    secret_names = [secret['Name'] for secret in list_secrets['SecretList']]
    assert "our_secret" in secret_names
    assert "your_secret" in secret_names


@mock_aws
def test_secret_can_be_retrieved():
    store_secret(sm_client, "my_secret", "keen_green_bean_1", "pa55word")
    store_secret(sm_client, "our_secret", "keen_green_bean_2", "pa55word")
    store_secret(sm_client, "your_secret", "keen_green_bean_3", "pa55word")

    output = retrieve_secret(sm_client, "my_secret")
    assert output['user'] == "keen_green_bean_1"
    assert output['password'] == "pa55word"

    output = retrieve_secret(sm_client, "our_secret")
    assert output['user'] == "keen_green_bean_2"
    assert output['password'] == "pa55word"

    output = retrieve_secret(sm_client, "your_secret")
    assert output['user'] == "keen_green_bean_3"
    assert output['password'] == "pa55word"
