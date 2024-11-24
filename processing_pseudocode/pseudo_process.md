INGESTION OUTPUT:
{
  "HasNewRows": {
    "counterparty": false,
    "currency": false,
    "department": false,
    "design": false,
    "staff": false,
    "sales_order": true,
    "address": false,
    "payment": true,
    "purchase_order": true,
    "payment_type": false,
    "transaction": true
  },
  "LastCheckedTime": "2024-11-21 09:47:38.018334"
}

iterate over HasNewRows

## DESIGN UPDATE IN INGESTION
--> if "design" is True, then
-----> create a pandas dataframe
-----> read design json named with LastCheckedTime directly into dataframe
-----> index = row ids
-----> write to parquet in dim_design folder with last-checked time as name

## COUNTERPARTY UPDATE IN INGESTION
--> if "counterparty" is True, then
-----> read counterparty json named with LastCheckedTime into dataframe
-----> extract series of address_ids from legal_address_id column + pass to row fetcher
-----> delete unwanted columns
-----> add address lines 1+2, district, city, postal code, country and phone no columns
-----> populate them with data from fetched address rows
-----> write to parquet in dim_counterparty folder with last-checked time as name

## ADDRESS UPDATE IN INGESTION
--> if "address" is True, then
-----> read address json named with LastCheckedTime into dataframe
-----> rename "address_id" column to "location_id"
-----> delete created_at and last_updated columns
-----> write to parquet in dim_location folder with last-checked time as name

# note: might be clearer to call 'exclusion list' 'already-updated list'
-----> get list of counterparty_ids included in latest update and add to exclusion list
-----> get list of s3 objects in counterparty folder of ingestion bucket
-----> iterate over them from newest to oldest, ignoring ids on exclusion list
-----> within objects, iterate over rows from newest to oldest
-----> find any row that references an address_id included in this update
-----> add that row with address columns updated to output dataframe
-----> add any counterparty_id that we've updated to the exclusion list
-----> check counterparty parquet
-----> write output dataframe to counterparty parquet folder with last-checked time as name





-----> pandas.dataframe(columns=["design_id", "design_name", "file_location", "file_name"])