import boto3
import os
import json

sqs = boto3.client('sqs', region_name='us-east-1')  # Substitua pelo seu AWS_REGION
queue_url = os.getenv('SQS_QUEUE_URL')

def enviar_mensagem_sqs(event_type, data):
    message = {
        'event_type': event_type,
        'data': data
    }
    sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps(message)
    )
