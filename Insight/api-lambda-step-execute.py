import boto3
import json

step_functions_client = boto3.client('stepfunctions')

def lambda_handler(event, context):
    body = json.loads(event['body'])
    youtube_url = body['youtube_url']
    
    response = step_functions_client.start_execution(
        stateMachineArn='arn:aws:states:us-east-1:590184144410:stateMachine:MyStateMachine-dm1ayly4p', # Update to your Step Function ARN
        input=json.dumps({'youtube_url': youtube_url})
    )
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'message': 'Transcription job started. You can check the status and results.',
            'executionArn': response['executionArn']
        })
    }

