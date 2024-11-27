resource "null_resource" "create_dependencies" {
  provisioner "local-exec" {
    command = "python --version && pip install -r ${path.module}/../requirements.txt -t ${path.module}/../dependencies/python"
  }

  triggers = {
    dependencies = filemd5("${path.module}/../requirements.txt")
  }
}


data "archive_file" "layer_code" {
  type        = "zip"
  output_path = "${path.module}/../packages/layer/layer.zip"
  source_dir  = "${path.module}/../dependencies"
}


# data "archive_file" "processing_layer_code" {
#   type        = "zip"
#   output_path = "${path.module}/../packages/layer/processing-layer.zip"
#   source_dir  = "${path.module}/../dependencies"
# }


resource "aws_lambda_layer_version" "dependencies" {
  layer_name       = "dependencies-layer"
  s3_bucket        = aws_s3_object.lambda_layer.bucket
  s3_key           = aws_s3_object.lambda_layer.key
  source_code_hash = data.archive_file.layer_code.output_base64sha256
}

resource "aws_lambda_layer_version" "processing_dependencies" {
  layer_name = "processing-dependencies-layer"
  s3_bucket  = aws_s3_object.processing_lambda_layer.bucket
  s3_key     = aws_s3_object.processing_lambda_layer.key
}