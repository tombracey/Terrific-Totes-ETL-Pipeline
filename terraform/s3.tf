resource "aws_s3_bucket" "code_bucket" {
  bucket_prefix = var.code_bucket_prefix
  tags  = {
    Name = "code_bucket"
  }
}

resource "aws_s3_bucket" "ingestion_bucket" {
    bucket_prefix = var.ingestion_bucket_prefix
    tags = {
        Name = "ingestion_bucket"
    }
}
