import boto3
import json

transcribe_client = boto3.client('transcribe')

def lambda_handler(event, context):
    job_name = event['job_name']
    response = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
    status = response['TranscriptionJob']['TranscriptionJobStatus']
    
    return {'job_name': job_name, 'status': status}

