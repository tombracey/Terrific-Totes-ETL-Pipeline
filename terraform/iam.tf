# LAMBDA POLICY AND ROLE
data "aws_iam_policy_document" "trust_policy" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
  
}


resource "aws_iam_role" "ingestion_lambda_role" {
  name_prefix        = "role-${var.ingestion_lambda_name}"
  assume_role_policy = data.aws_iam_policy_document.trust_policy.json
}

# LAMBDA s3 WRITE PERMISSIONS AND ATTACHMENT

data "aws_iam_policy_document" "s3_data_policy_doc" {
  statement {
    actions = ["s3:*"]
    resources = [aws_s3_bucket.ingestion_bucket.arn]
  }
}
# we have given permission to write into any s3 bucket, 

resource "aws_iam_policy" "s3_write_policy" {
  name_prefix = "s3-policy-${var.ingestion_lambda_name}-write"
  policy      = data.aws_iam_policy_document.s3_data_policy_doc.json
}


resource "aws_iam_role_policy_attachment" "lambda_s3_write_policy_attachment" {
    role = aws_iam_role.ingestion_lambda_role.name
    policy_arn = aws_iam_policy.s3_write_policy.arn
}


# CLOUDWATCH LOGS POLICY AND ATTACHMENT TO LAMBDA ROLE

resource "aws_cloudwatch_log_group" "ingestion_lambda_log_group"{
  name = "/aws/lambda/${var.ingestion_lambda_name}"
}


data "aws_iam_policy_document" "cloudwatch_logs_policy_document" {
  statement {
    sid = "1"

    actions = [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
    ]

    resources = [
      "*"
    ]
  }
  }


resource "aws_iam_policy" "cloudwatch_logs_policy" {
  name   = "cloudwatch_logs_policy"
  policy = data.aws_iam_policy_document.cloudwatch_logs_policy_document.json
}


resource "aws_iam_role_policy_attachment" "lambda_cloudwatch_logs_policy_attachment" {
    role = aws_iam_role.ingestion_lambda_role.name
    policy_arn = aws_iam_policy.cloudwatch_logs_policy.arn
}



