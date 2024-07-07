import boto3
import json
import os
import logging

# Initialize clients for AWS services
transcribe_client = boto3.client('transcribe')
s3_client = boto3.client('s3')

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    job_name = event['pathParameters']['job_name']
    result_key = f"results/{job_name}.json"
    bucket_name = os.environ['RESULTS_BUCKET']
    
    try:
        # Check if the results file exists in S3
        s3_object = s3_client.get_object(Bucket=bucket_name, Key=result_key)
        result_data = json.loads(s3_object['Body'].read().decode('utf-8'))
        return {
            'statusCode': 200,
            'body': json.dumps(result_data)
        }
    except s3_client.exceptions.NoSuchKey:
        # If the results file does not exist, check the status of the transcription job
        try:
            response = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
            status = response['TranscriptionJob']['TranscriptionJobStatus']
            return {
                'statusCode': 200,
                'body': json.dumps({'status': status})
            }
        except Exception as e:
            logger.error(f"Error checking transcription job status: {e}")
            return {
                'statusCode': 500,
                'body': json.dumps({'error': 'Internal server error'})
            }

