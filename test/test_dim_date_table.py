from src.utils.dim_date_table import *
from datetime import date
import pg8000

def connect_to_test_dw():
    sm_client = boto3.client("secretsmanager", "eu-west-2")
    credentials = retrieve_secret(sm_client, "gb-ttotes/test-db-credentials")
    print(credentials["TEST_HOST"])

    return pg8000.connect(
        user=credentials["TEST_USER"],
        password=credentials["TEST_PASSWORD"],
        database=credentials["TEST_DATABASE"],
        host=credentials["TEST_HOST"],
        port=credentials["TEST_PORT"]
    )

def test_data_type_of_dim_date_columns():
    conn = connect_to_test_dw()
    test_input = insert_dim_date_table_into_data_warehouse(conn=connect_to_test_dw())
    query = "SELECT * FROM dim_date;"
    result = conn.run(query)
    assert type(result[0][0]) == date
    assert type(result[0][1]) == int
    assert type(result[0][2]) == int
    assert type(result[0][3]) == int
    assert type(result[0][4]) == int
    assert type(result[0][5]) == str
    assert type(result[0][6]) == str
    assert type(result[0][7]) == int

# def test_check_start_and_end_date():
#     conn = connect_to_dw()
#     query = "SELECT * FROM dim_date;"
#     result = conn.run(query)
    
