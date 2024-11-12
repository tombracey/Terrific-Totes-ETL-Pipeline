from src.connection import connect_to_db, close_connection
import datetime
import json

"""
TABLES TO INGEST
counterparty
currency
department
design
staff
sales_order
address
payment
purchase_order
payment_type
transaction
"""

def get_data():
    output_list = []
    db = connect_to_db()
    # test_db = db.run('SELECT * FROM counterparty;')
    # print(test_db)
    # for row in test_db:
    #     output_list.append({})

    # output_dict = {'counterparty': test_db}

    


    test_db = db.run(
        '''COPY (
            SELECT json_agg(row_to_json(counterparty))::text 
            FROM counterparty)
          ) TO XXXXXXXXX'''
    print(test_db)

    # with open('test_db.txt', 'w') as f:
    #     db_json = json.dumps(test_db, default=str)
    #     f.write(db_json)
    
    


get_data()