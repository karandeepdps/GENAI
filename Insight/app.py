import boto3
import json
import urllib.parse
import os
import time
import logging
from yt_dlp import YoutubeDL

# Initialize clients for AWS services
transcribe_client = boto3.client('transcribe')
comprehend_client = boto3.client('comprehend')
s3_client = boto3.client('s3')

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def download_youtube_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '/tmp/audio.%(ext)s',
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return '/tmp/audio.webm'  # yt-dlp default audio format might be webm
    except Exception as e:
        logger.error(f"Error downloading audio: {e}")
        raise

def upload_to_s3(file_path, bucket_name, object_name):
    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
        return f's3://{bucket_name}/{object_name}'
    except Exception as e:
        logger.error(f"Error uploading to S3: {e}")
        raise

def start_transcription_job(s3_uri, job_name):
    try:
        response = transcribe_client.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': s3_uri},
            MediaFormat='webm',  # Change to webm if the file format is webm
            LanguageCode='en-US',
            OutputBucketName=os.environ['TRANSCRIBE_OUTPUT_BUCKET']
        )
        logger.info(f"Started transcription job: {response}")
        return response
    except Exception as e:
        logger.error(f"Error starting transcription job: {e}")
        raise

def get_transcription_text(job_name):
    try:
        while True:
            response = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
            status = response['TranscriptionJob']['TranscriptionJobStatus']
            if status == 'COMPLETED':
                transcript_uri = response['TranscriptionJob']['Transcript']['TranscriptFileUri']
                parsed_url = urllib.parse.urlparse(transcript_uri)
                bucket_name = os.environ['TRANSCRIBE_OUTPUT_BUCKET']
                object_key = parsed_url.path.split('/')[-1]
                
                logger.info(f"Transcript URI: {transcript_uri}")
                logger.info(f"Bucket Name: {bucket_name}")
                logger.info(f"Object Key: {object_key}")
                
                # Retrieve the transcription file directly from S3
                s3_object = s3_client.get_object(Bucket=bucket_name, Key=object_key)
                transcript_json = s3_object['Body'].read().decode('utf-8')
                transcript_data = json.loads(transcript_json)
                return transcript_data['results']['transcripts'][0]['transcript']
            elif status == 'FAILED':
                raise Exception('Transcription job failed')
            time.sleep(15)
    except Exception as e:
        logger.error(f"Error getting transcription text: {e}")
        raise

def extract_insights(text):
    try:
        response = comprehend_client.detect_key_phrases(Text=text, LanguageCode='en')
        key_phrases = response['KeyPhrases']
        return key_phrases
    except Exception as e:
        logger.error(f"Error extracting insights: {e}")
        raise

def lambda_handler(event, context):
    event=json.loads(event['body'])
    youtube_url = event['youtube_url']
    
    # Download the audio from YouTube
    audio_file_path = download_youtube_audio(youtube_url)
    
    # Upload the audio file to S3
    s3_uri = upload_to_s3(audio_file_path, os.environ['AUDIO_BUCKET'], 'customer_interview.webm')
    
    # Start transcription job
    job_name = 'transcription_job_' + str(int(time.time()))
    start_transcription_job(s3_uri, job_name)
    
    # Get the transcription text
    transcription_text = get_transcription_text(job_name)
    
    # Extract insights from the transcribed text
    insights = extract_insights(transcription_text)
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'transcription': transcription_text,
            'insights': insights
        })
    }
