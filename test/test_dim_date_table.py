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
        database=credentials["TEST_DB"],
        host=credentials["TEST_HOST"],
        port=credentials["TEST_PORT"],
    )

def connect_to_db():
    sm_client = boto3.client("secretsmanager", "eu-west-2")
    credentials = retrieve_secret(sm_client, "gb-ttotes/totesys-olap-credentials")
    return pg8000.connect(
        user=credentials["DW_USER"],
        password=credentials["DW_PASSWORD"],
        database=credentials["DW_DATABASE"],
        host=credentials["DW_HOST"],
        port=credentials["DW_PORT"],
    )

def test_data_type_of_dim_date_columns():
    conn = connect_to_test_dw()
    insert_dim_date_table_into_data_warehouse(conn)
    query = "SELECT * FROM dim_date;"
    result = conn.run(query)
    print(result)
    # assert type(result[0][0]) == date
    # assert type(result[0][1]) == int
    # assert type(result[0][2]) == int
    # assert type(result[0][3]) == int
    # assert type(result[0][4]) == int
    # assert type(result[0][5]) == str
    # assert type(result[0][6]) == str
    # assert type(result[0][7]) == int

# def test_check_start_and_end_date():
#     conn = connect_to_dw()
#     start_query = "SELECT MIN(date_id) FROM dim_date;"
#     end_query = "SELECT MAX(date_id) FROM dim_date;"
#
#     assert conn.run(start_query) == '2024-11-11'
#     assert conn.run(end_query) == '2030-12-31'
    
