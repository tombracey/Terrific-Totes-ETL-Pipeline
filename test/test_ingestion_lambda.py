from src.ingestion_lambda import *
from src.connection import connect_to_db, close_connection
import datetime
import pytest
from unittest.mock import patch, Mock


@pytest.fixture()
def test_table():
    db = connect_to_db()
    table = db.run('''CREATE TABLE IF NOT EXISTS test_table
    AS (SELECT * FROM counterparty);''')
    close_connection(db)
    return table

def test_connection_can_access_table():
    test_db = connect_to_db()
    query = "SELECT * FROM counterparty LIMIT 3;"
    expect = test_db.run(query)
    # print(expect)
    assert type(expect[0][0]) == int
    assert type(expect[0][1]) == str
    assert type(expect[0][2]) == int
    assert type(expect[0][3]) == str
    assert type(expect[0][4]) == str
    assert type(expect[0][5]) == datetime.datetime
    assert type(expect[0][6]) == datetime.datetime


dummy_counterparty_table = [[1, 'Fahey and Sons', 15, 'Micheal Toy', 'Mrs. Lucy Runolfsdottir', datetime.datetime(2022, 11, 3, 14, 20, 51, 563000), datetime.datetime(2022, 11, 3, 14, 20, 51, 563000)], [2, 'Dummy LPR', 28, 'Melba Sanford', 'Jean Hane III', datetime.datetime(2024, 11, 3, 14, 20, 51, 563000), datetime.datetime(2024, 11, 3, 14, 20, 51, 563000)], [3, 'Armstrong Inc', 2, 'Jane Wiza', 'Myra Kovacek', datetime.datetime(2022, 11, 3, 14, 20, 51, 563000), datetime.datetime(2022, 11, 3, 14, 20, 51, 563000)]]

connection = Mock()
connection.run.return_value = dummy_counterparty_table
connection.columns = [{"name": "id"}, {"name":"dd"}]

# @patch("src.ingestion_lambda.connect_to_db", return_value=connection)
def test_ingests_updated_rows_of_counterparty_table():
    # get_counterparty()
    # patcher = patch("src.ingestion_lambda", return_value=dummy_counterparty_table)
    # patcher.start()
    test_datetime = datetime.datetime(2023, 11, 3, 14, 20, 51, 563000)
    test_datetime = '2023-11-03'
    print(get_data(test_datetime)['counterparty'])
    assert get_data(test_datetime)['counterparty'] == [[2, 'Dummy LPR', 28, 'Melba Sanford', 'Jean Hane III', datetime.datetime(2024, 11, 3, 14, 20, 51, 563000), datetime.datetime(2024, 11, 3, 14, 20, 51, 563000)]]
    