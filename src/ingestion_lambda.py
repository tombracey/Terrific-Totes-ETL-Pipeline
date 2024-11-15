def ingestion_lambda_handler():
    db = connect_to_db()
    sm_client = boto3.client('secretsmanager')
    last_updated_secret = retrieve_secret(sm_client, 'last_update')
    last_update = last_updated_secret['last_update']

    date_and_time = datetime.datetime.now().strftime()
    update_secret(sm_client, 'last_update', ['last_update', date_and_time])
    
    data = get_data(db, last_update)
    
    for table in data:
        rows = data[table][0]
        columns = data[table][1]
        new_rows = []
        for row in rows:
            new_rows.append(date_to_strftime(row))
        zipped_dict = zip_dictionary(new_rows, columns)
        json_data = format_to_json(zipped_dict)
        file_name = datetime.datetime.now().strftime()
        folder_name = table
        s3_client = boto3.client('s3')
        json_to_s3(s3_client, json_data, "green-bean-ingestion-bucket", folder_name, file_name)



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


def get_data(db, last_update):

    data = {}
    counterparty = db.run("SELECT * FROM counterparty WHERE last_updated >= :last_update;", last_update = last_update)
    data["counterparty"] = (counterparty, [col['name'] for col in db.columns])

    currency = db.run("SELECT * FROM currency WHERE last_updated >= :last_update;", last_update = last_update)
    data["currency"] = (currency, [col['name'] for col in db.columns])

    department = db.run("SELECT * FROM department WHERE last_updated >= :last_update;", last_update = last_update)
    data["department"] = (department, [col['name'] for col in db.columns])

    design = db.run("SELECT * FROM design WHERE last_updated >= :last_update;", last_update = last_update)
    data["design"] = (design, [col['name'] for col in db.columns]) 
    
    staff = db.run("SELECT * FROM staff WHERE last_updated >= :last_update;", last_update = last_update)
    data["staff"] = (staff, [col['name'] for col in db.columns])

    sales_order = db.run("SELECT * FROM sales_order WHERE last_updated >= :last_update;", last_update = last_update)
    data["sales_order"] = (sales_order, [col['name'] for col in db.columns])

    address = db.run("SELECT * FROM address WHERE last_updated >= :last_update;", last_update = last_update)
    data["address"] = (address, [col['name'] for col in db.columns])

    payment = db.run("SELECT * FROM payment WHERE last_updated >= :last_update;", last_update = last_update)
    data["payment"] = (payment, [col['name'] for col in db.columns])

    purchase_order = db.run("SELECT * FROM purchase_order WHERE last_updated >= :last_update;", last_update = last_update)
    data["purchase_order"] = (purchase_order, [col['name'] for col in db.columns])
   
    payment_type = db.run("SELECT * FROM payment_type WHERE last_updated >= :last_update;", last_update = last_update)
    data["payment_type"] = (payment_type, [col['name'] for col in db.columns])
  
    transaction = db.run("SELECT * FROM transaction WHERE last_updated >= :last_update;", last_update = last_update)
    data["transaction"] = (transaction, [col['name'] for col in db.columns])

    return data



