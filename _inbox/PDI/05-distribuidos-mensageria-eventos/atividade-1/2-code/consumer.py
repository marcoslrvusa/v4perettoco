import json
def consume(sqs, queue, dlq, prefetch=10):
    msgs = sqs.receive_message(QueueUrl=queue, MaxNumberOfMessages=prefetch)
    for m in msgs.get("Messages", []):
        try:
            handle(json.loads(m["Body"]))
            sqs.delete_message(QueueUrl=queue, ReceiptHandle=m["ReceiptHandle"])
        except Exception:
            sqs.send_message(QueueUrl=dlq, MessageBody=m["Body"])
