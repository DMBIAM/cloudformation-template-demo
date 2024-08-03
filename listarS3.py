import json
import boto3

s3 = boto3.client('s3')
bucket_name = 's3demo'

def handler(event, context):
    objects = s3.list_objects_v2(Bucket=bucket_name)
    return {
        'statusCode': 200,
        'body': json.dumps(objects['Contents'])
    }
