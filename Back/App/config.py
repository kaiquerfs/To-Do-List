import os

class Config:
    AWS_REGION = os.getenv('AWS_REGION', 'Minha região')
    S3_BUCKET = os.getenv('S3_BUCKET')
    SQS_QUEUE_URL = os.getenv('Url da Fila')
    DYNAMODB_TABLE = os.getenv('DYNAMODB_TABLE', 'todo_tasks')
