variable "state_bucket_name" {
    type = string
    default = "gb-ttotes-remote-state-bucket"
}

variable "ingestion_lambda_name" {
    type = string
    default = "gb-ttotes-ingestion-lambda"
}

variable "ingestion_code_bucket_prefix" {
    type = string
    default = "code-bucket-ingestion-lambda"
}

variable "python_runtime" {
  type    = string
  default = "python3.12"
}

variable "ingestion_bucket_prefix" {
    type = string
    default = "ingestion-bucket"
}