import boto3
import json
import os
import time
import logging
from yt_dlp import YoutubeDL

transcribe_client = boto3.client('transcribe')
s3_client = boto3.client('s3')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def download_youtube_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '/tmp/audio.%(ext)s',
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return '/tmp/audio.webm'

def upload_to_s3(file_path, bucket_name, object_name):
    s3_client.upload_file(file_path, bucket_name, object_name)
    return f's3://{bucket_name}/{object_name}'

def lambda_handler(event, context):
    youtube_url = event['youtube_url']
    job_name = 'transcription_job_' + str(int(time.time()))
    
    audio_file_path = download_youtube_audio(youtube_url)
    s3_uri = upload_to_s3(audio_file_path, os.environ['AUDIO_BUCKET'], 'customer_interview.webm')
    
    transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': s3_uri},
        MediaFormat='webm',
        LanguageCode='en-US',
        OutputBucketName=os.environ['TRANSCRIBE_OUTPUT_BUCKET']
    )
    
    return {'job_name': job_name}

