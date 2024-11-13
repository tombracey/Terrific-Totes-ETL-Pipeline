data "archive_file" "ingestion_lambda_zip" {
  type             = "zip"
  output_file_mode = "0666"
  source_file      = "${path.module}/../src/dummy_lambda_handler.py"
  output_path      = "${path.module}/../packages/ingestion/function.zip"
}


