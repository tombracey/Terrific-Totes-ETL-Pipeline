from datetime import datetime

def datetime_to_strftime(rows):
    new_rows = rows.copy()
    for row in new_rows:
        for item in row:
            if isinstance(item, datetime):
                new_item = item.strftime("%Y-%m-%d %H:%M:%S")
                item_index = row.index(item)
                row[item_index] = new_item
    return new_rows


def zip_dictionary(new_rows, columns):
    
    zipped_dict = [dict(zip(columns, row)) for row in new_rows]
    
    return zipped_dict

