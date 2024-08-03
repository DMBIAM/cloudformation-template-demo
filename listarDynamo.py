import json
import boto3

dynamodb = boto3.client('dynamodb')
table_name = 'productos'

def handler(event, context):
    response = dynamodb.scan(TableName=table_name)
    return {
        'statusCode': 200,
        'body': json.dumps(response['Items'])
    }
