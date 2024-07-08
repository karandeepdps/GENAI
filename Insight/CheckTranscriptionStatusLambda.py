import boto3
import json

transcribe_client = boto3.client('transcribe')

def lambda_handler(event, context):
    job_name = event['transcription']['job_name']
    recipient_email = event['transcription']['recipient_email']
    
    response = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
    status = response['TranscriptionJob']['TranscriptionJobStatus']
    
    return {
        'status': status,
        'recipient_email': recipient_email
    }
