
def zip_dictionary(rows, columns):
    
    zipped_dict = [dict(zip(columns, row)) for row in rows]
    
    return zipped_dict
