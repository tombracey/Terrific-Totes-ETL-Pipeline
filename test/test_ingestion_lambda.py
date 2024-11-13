from src.ingestion_lambda import *
from src.connection import connect_to_db, close_connection
from datetime import datetime
import pytest

@pytest.fixture()
def test_table():
    db = connect_to_db()
    table = db.run('''CREATE TABLE IF NOT EXISTS test_table
    AS (SELECT * FROM counterparty);''')
    close_connection(db)
    return table

def test_connection_can_access_table():
    test_db = connect_to_db()
    query = "SELECT * FROM counterparty LIMIT 1;"
    expect = test_db.run(query)
    print(expect)
    assert type(expect[0][0]) == int
    assert type(expect[0][1]) == str
    assert type(expect[0][2]) == int
    assert type(expect[0][3]) == str
    assert type(expect[0][4]) == str
    assert type(expect[0][5]) == datetime.datetime
    assert type(expect[0][6]) == datetime.datetime

def test_ingests_updated_rows_of_counterparty_table():
    pass