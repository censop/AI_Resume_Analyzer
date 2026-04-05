import json
import boto3
import uuid
import traceback
from botocore.config import Config

def lambda_handler(event, context):
    try:
        s3_client = boto3.client('s3', region_name='us-east-1', config=Config(signature_version='s3v4'))
        BUCKET_NAME = "resume-analyzer-file-upload-bucket" 
        
        file_id = str(uuid.uuid4())
        file_key = f"uploads/{file_id}.txt"
        result_key = f"results/{file_id}.txt.json" 
        
        presigned_upload_url = s3_client.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': BUCKET_NAME,
                'Key': file_key,
                'ContentType': 'text/plain',
            },
            ExpiresIn=300
        )
        
        presigned_download_url = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': BUCKET_NAME,
                'Key': result_key
            },
            ExpiresIn=3600
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'uploadUrl': presigned_upload_url,
                'downloadUrl': presigned_download_url,
                'fileKey': file_key
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e),
                'trace': traceback.format_exc()
            })
        }
