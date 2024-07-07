import boto3
import json

step_functions_client = boto3.client('stepfunctions')

def lambda_handler(event, context):
    body = json.loads(event['body'])
    execution_arn = body['executionArn']
    
    response = step_functions_client.describe_execution(
        executionArn=execution_arn
    )
    
    if response['status'] == 'SUCCEEDED':
        output = json.loads(response['output'])
    else:
        output = {'status': response['status']}
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(output)
    }

