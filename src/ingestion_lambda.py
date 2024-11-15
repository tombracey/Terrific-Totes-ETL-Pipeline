
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
    counterparty = db.run("SELECT * FROM counterparty WHERE last_updated > :last_update;", last_update = last_update)
    data["counterparty"] = (counterparty, [col['name'] for col in db.columns])

    currency = db.run("SELECT * FROM currency WHERE last_updated > :last_update;", last_update = last_update)
    data["currency"] = (currency, [col['name'] for col in db.columns])

    department = db.run("SELECT * FROM department WHERE last_updated > :last_update;", last_update = last_update)
    data["department"] = (department, [col['name'] for col in db.columns])

    design = db.run("SELECT * FROM design WHERE last_updated > :last_update;", last_update = last_update)
    data["design"] = (design, [col['name'] for col in db.columns]) 
    
    staff = db.run("SELECT * FROM staff WHERE last_updated > :last_update;", last_update = last_update)
    data["staff"] = (staff, [col['name'] for col in db.columns])

    sales_order = db.run("SELECT * FROM sales_order WHERE last_updated > :last_update;", last_update = last_update)
    data["sales_order"] = (sales_order, [col['name'] for col in db.columns])

    address = db.run("SELECT * FROM address WHERE last_updated > :last_update;", last_update = last_update)
    data["address"] = (address, [col['name'] for col in db.columns])

    payment = db.run("SELECT * FROM payment WHERE last_updated > :last_update;", last_update = last_update)
    data["payment"] = (payment, [col['name'] for col in db.columns])

    purchase_order = db.run("SELECT * FROM purchase_order WHERE last_updated > :last_update;", last_update = last_update)
    data["purchase_order"] = (purchase_order, [col['name'] for col in db.columns])
   
    payment_type = db.run("SELECT * FROM payment_type WHERE last_updated > :last_update;", last_update = last_update)
    data["payment_type"] = (payment_type, [col['name'] for col in db.columns])
  
    transaction = db.run("SELECT * FROM transaction WHERE last_updated > :last_update;", last_update = last_update)
    data["transaction"] = (transaction, [col['name'] for col in db.columns])

    return data



