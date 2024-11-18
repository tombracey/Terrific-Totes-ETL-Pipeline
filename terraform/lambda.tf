resource "aws_lambda_function" "ingestion_lambda" {

  function_name = var.ingestion_lambda_name
  role          = aws_iam_role.ingestion_lambda_role.arn
  s3_bucket = aws_s3_bucket.code_bucket.id
  s3_key = aws_s3_object.ingestion_lambda_code.key
  handler       = "${var.ingestion_lambda_filename}.ingestion_lambda_handler"
  runtime = var.python_runtime
  timeout = 60
  source_code_hash = filebase64sha256("${path.module}/../src/${var.ingestion_lambda_filename}.py")
  publish = true

  environment {
      variables = {
        INGESTION_BUCKET_NAME = aws_s3_bucket.ingestion_bucket.id
      }
    }

}



# we think we will need to add a layers= to this once layer is completed


