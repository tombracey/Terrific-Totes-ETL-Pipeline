import  boto3, os

def json_to_s3(data, bucket_name):
    
    with open(f"{os.getcwd()}/{data}.json", "w", encoding="UTF-8") as file:
        file.write(data)

    s3 = boto3.resource('s3')    
    s3.Bucket(bucket_name).upload_file(f"{os.getcwd()}/{data}.json", bucket_name,f"{data}.json")
   
   #file name for s3 needs date time ingested