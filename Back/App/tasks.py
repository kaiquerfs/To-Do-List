import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
import os
import uuid

# Configuração do DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')  # Substitua pelo seu AWS_REGION
table_name = os.getenv('DYNAMODB_TABLE', 'Todos')
table = dynamodb.Table(table_name)

def obter_tarefas():
    try:
        response = table.scan()
        return response.get('Items', [])
    except ClientError as e:
        print(f"Erro ao obter tarefas: {e.response['Error']['Message']}")
        return []

def criar_tarefa(tarefa):
    try:
        table.put_item(Item=tarefa)
    except ClientError as e:
        print(f"Erro ao criar tarefa: {e.response['Error']['Message']}")

def atualizar_tarefa(tarefa_id, tarefa_atualizada):
    try:
        response = table.update_item(
            Key={'id': tarefa_id},
            UpdateExpression="set task=:t, completed=:c",
            ExpressionAttributeValues={
                ':t': tarefa_atualizada['task'],
                ':c': tarefa_atualizada['completed']
            },
            ReturnValues="UPDATED_NEW"
        )
        return response
    except ClientError as e:
        print(f"Erro ao atualizar tarefa: {e.response['Error']['Message']}")

def deletar_tarefa(tarefa_id):
    try:
        table.delete_item(Key={'id': tarefa_id})
    except ClientError as e:
        print(f"Erro ao deletar tarefa: {e.response['Error']['Message']}")
