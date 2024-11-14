from datetime import datetime

# for row in new_rows:
def datetime_to_strftime(row):
    new_row = row.copy()
    for i in range(len(row)):
        if isinstance(row[i], datetime):
            new_item = row[i].strftime("%Y-%m-%d %H:%M:%S:%f")
            new_row[i] = new_item
    return new_row


def zip_dictionary(new_rows, columns):
    
    zipped_dict = [dict(zip(columns, row)) for row in new_rows]
    
    return zipped_dict

