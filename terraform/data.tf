data "archive_file" "lambda" {
  type             = "zip"
  output_file_mode = "0666"
  source_file      = "${path.module}/../src/dummy_lambda_handler.py"
  output_path      = "${path.module}/../function.zip"
}

# do we need a function.zip file?
