resource "aws_sqs_queue" "uploads" {
  name = "uploads"
  visibility_timeout_seconds = 300
  redrive_policy = jsonencode({ deadLetterTargetArn = aws_sqs_queue.uploads_dlq.arn, maxReceiveCount = 3 })
}
resource "aws_lambda_function" "process" {
  function_name = "process_upload"
  runtime = "python3.12"
  handler = "process_upload.handler"
  reserved_concurrent_executions = 10
}
