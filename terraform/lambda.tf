resource "aws_lambda_function" "ingestion_lambda" {

  function_name = var.ingestion_lambda_name
  role          = aws_iam_role.ingestion_lambda_role.arn
  s3_bucket = aws_s3_bucket.code_bucket.id
  s3_key = aws_s3_object.ingestion_lambda_code.key
  handler       = "dummy_lambda_handler.lambda_handler"
  runtime = var.python_runtime
  timeout = 60
  source_code_hash = filebase64sha256("${path.module}/../src/dummy_lambda_handler.py")
  publish = true
}
# we think we will need to add a layers= to this once layer is completed


resource "aws_s3_object" "ingestion_lambda_code" {
  bucket = aws_s3_bucket.code_bucket.id
  key    = "function.zip"
  source = "${path.module}/../packages/ingestion/function.zip" 
  etag = filemd5(data.archive_file.ingestion_lambda_zip.output_path)
}

