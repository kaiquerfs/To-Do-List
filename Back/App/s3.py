import boto3
import os

s3 = boto3.client('s3', region_name='Colocar a região do S3 Aqui')  
bucket_name = os.getenv('Colocar nome do meu S3 depois')

def fazer_upload_s3(file):
    file_key = file.filename
    s3.upload_fileobj(file, bucket_name, file_key)
    file_url = f"https://{bucket_name}.s3.amazonaws.com/{file_key}"
    return file_url

def baixar_arquivo_s3(file_key):
    file_path = f"/tmp/{file_key}"
    s3.download_file(bucket_name, file_key, file_path)
    return file_path
