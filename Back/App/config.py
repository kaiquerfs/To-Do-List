import os

class Config:
    AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
    S3_BUCKET = os.getenv('S3_BUCKET')
    SQS_QUEUE_URL = os.getenv('SQS_QUEUE_URL')
    DYNAMODB_TABLE = os.getenv('DYNAMODB_TABLE', 'todo_tasks')
