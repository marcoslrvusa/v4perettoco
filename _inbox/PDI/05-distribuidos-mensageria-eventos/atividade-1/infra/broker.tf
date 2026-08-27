resource "aws_sqs_queue" "events" {
  name = "events"
  visibility_timeout_seconds = 60
  redrive_policy = jsonencode({ deadLetterTargetArn = aws_sqs_queue.events_dlq.arn, maxReceiveCount = 3 })
}
