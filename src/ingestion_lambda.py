from src.connection import connect_to_db, close_connection
from datetime import datetime, timedelta
import json
import boto3
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

# last_update = datetime.now() - timedelta(minutes = 20)
# print(last_update)
last_update = datetime(2023, 11, 3, 14, 20, 51, 563000)

start_date = last_update
end_date = datetime.now()

def get_counterparty():
    db = connect_to_db()
    counterparty = db.run("SELECT * FROM counterparty;")
    print(counterparty)
    col_names = [col['name'] for col in db.columns]
    print(col_names)
    return counterparty

def get_data(last_update):
    db = connect_to_db()

    # counterparty = db.run("SELECT * FROM counterparty WHERE last_updated > :last_update;", last_update = last_update)

    counterparty = db.run(f"SELECT * FROM counterparty WHERE last_updated > '{last_update}';")

    currency = db.run("SELECT * FROM currency;")
    department = db.run("SELECT * FROM department;")
    design = db.run("SELECT * FROM design;")
    staff = db.run("SELECT * FROM staff;")
    sales_order = db.run("SELECT * FROM sales_order;")
    address = db.run("SELECT * FROM address;")
    payment = db.run("SELECT * FROM payment;")
    purchase_order = db.run("SELECT * FROM purchase_order;")
    payment_type = db.run("SELECT * FROM payment_type;")
    transaction = db.run("SELECT * FROM transaction;")

    data = {}
    data["counterparty"] = counterparty
    data["currency"] = currency
    data["department"] = department
    data["design"] = design
    data["staff"] = staff
    data["sales_order"] = sales_order
    data["address"] = address
    data["payment"] = payment
    data["purchase_order"] = purchase_order
    data["payment_type"] = payment_type
    data["transaction"] = transaction
    
    return data

get_data(last_update)    

# def get_data():
#     output_list = []
#     db = connect_to_db()
#     test_db = db.run('''
#         SELECT json_agg(row_to_json(counterparty))::text
#         FROM counterparty
#         );''')
   
#     # print(test_db)
#     # for row in test_db:
#     # output_list.append({})
#     # output_dict = {'counterparty': test_db}
    

#     with open('totesys.json', 'w') as f:
#         db_json = json.dumps(<data>, default=str)
#         f.write(db_json)


#     s3 = boto3.client('s3')
#     s3.put_object(Body=json_data, Bucket=bucket_name, Key=file_name)
#     return {
#         'statusCode': 200,
#         'body': 'File uploaded successfully.'
#         }