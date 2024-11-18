resource "aws_iam_role" "state_machine_role" {
    name_prefix = "role-ttotes-state-machine-"
    assume_role_policy = <<EOF
    {
        attached_policy = true
        state_machine_policy = jsonencode({
        "Version": "2012-10-17",
        "Statement": [
            {
            "Effect": "Allow",
            "Action": [
                "lambda:InvokeFunction"
            ],
            "Resource": "arn:aws:lambda:{aws_region}:{aws_account_num}:function:{function_name}"
            }
        ]
    }
    EOF
}

data "aws_iam_policy_document" "state_machine_role_policy" {
  
  statement {
    effect = "Allow"

    actions = [
      "lambda:InvokeFunction"
    ]

    resources = ["${state_machine_var.ingestion_lambda_name.arn}:*"]
  }
  
}


#resource "aws_iam_role" "state_machine_role" {
#  name_prefix        = "role-${state_machine_var.state_machine_name}"
#  assume_role_policy = data.aws_iam_policy_document.state_machine_role_policy.json
#}



