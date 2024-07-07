import boto3
import json
import os

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    job_name = event['job_name']
    transcription = event['transcription']
    insights = event['insights']
    
    final_results = {
        'status': 'COMPLETED',
        'transcription': transcription,
        'insights': insights
    }
    
    s3_client.put_object(Bucket=os.environ['RESULTS_BUCKET'], Key=f'results/{job_name}.json', Body=json.dumps(final_results))
    
    return {'status': 'COMPLETED'}

