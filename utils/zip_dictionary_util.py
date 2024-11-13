
def zip_dictionary(rows, coloumns):
    
    zipped_dict = [dict(zip(coloumns, row)) for row in rows]
    return zipped_dict