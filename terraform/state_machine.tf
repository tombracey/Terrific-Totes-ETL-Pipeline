
resource "aws_sfn_state_machine" "sfn_state_machine" {
  name_prefix = "var.state_machine_name"
  definition = templatefile("${path.module}/statemachine/state_machine.json",
    { aws_region        = data.aws_region.current.name,
      aws_account_num   = data.aws_caller_identity.current.account_id,
      function_name     = var.ingestion_lambda_name
    })
  role_arn = aws_iam_role.step_function_role.arn
}
