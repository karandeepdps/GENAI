import boto3
import json
import urllib.parse
import os

s3_client = boto3.client('s3')
comprehend_client = boto3.client('comprehend')
transcribe_client = boto3.client('transcribe')


def get_transcription_text(job_name):
    response = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
    transcript_uri = response['TranscriptionJob']['Transcript']['TranscriptFileUri']
    parsed_url = urllib.parse.urlparse(transcript_uri)
    bucket_name = os.environ['TRANSCRIBE_OUTPUT_BUCKET']
    object_key = parsed_url.path.split('/')[-1]
    
    s3_object = s3_client.get_object(Bucket=bucket_name, Key=object_key)
    transcript_json = s3_object['Body'].read().decode('utf-8')
    transcript_data = json.loads(transcript_json)
    return transcript_data['results']['transcripts'][0]['transcript']

def extract_insights(text):
    response = comprehend_client.detect_key_phrases(Text=text, LanguageCode='en')
    return response['KeyPhrases']

def lambda_handler(event, context):
    job_name = event['job_name']
    transcription_text = get_transcription_text(job_name)
    insights = extract_insights(transcription_text)
    
    return {'job_name': job_name, 'transcription': transcription_text, 'insights': insights}

