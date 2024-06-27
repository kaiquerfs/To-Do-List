import boto3
import os
import json

sqs = boto3.client('sqs', region_name='Colocar a região da minha fila')  
queue_url = os.getenv('Colocar minha URL da fila aqui')

def enviar_mensagem_sqs(event_type, data):
    message = {
        'event_type': event_type,
        'data': data
    }
    sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps(message)
    )
