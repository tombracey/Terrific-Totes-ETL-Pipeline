from src.utils.dim_date_table import *
from datetime import date

def test_data_type_of_dim_date_columns():
    test_input = insert_dim_date_table_into_data_warehouse()
    conn = connect_to_dw()
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

def test_check_start_and_end_date():
    conn = connect_to_dw()
    query = "SELECT * FROM dim_date;"
    result = conn.run(query)
    
