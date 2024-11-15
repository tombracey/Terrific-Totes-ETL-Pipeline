import  boto3, os

""" takes json string, writes as local file and then uploads to s3 bucket;
    name of table data has come from, 
    bucket name data to be uploaded to,
    folder - path in bucket
    file_name - name of data when stored in bucket """


def json_to_s3(client, json_string, bucket_name, folder, file_name):
    
    with open(f"{os.getcwd()}/{file_name}", "w", encoding="UTF-8") as file:
        file.write(json_string)

  
    response = client.upload_file(f"{os.getcwd()}/{file_name}", bucket_name,f"{folder}/{file_name}")
   
    os.remove(f"{os.getcwd()}/{file_name}")
    
    return response
   #(file name for s3 in main function will need date time ingested)