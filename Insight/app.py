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
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return '/tmp/audio.mp3'
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
            MediaFormat='mp3',
            LanguageCode='en-US',
            OutputBucketName=os.environ['TRANSCRIBE_OUTPUT_BUCKET']
        )
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
                transcript_json = urllib.request.urlopen(transcript_uri).read().decode('utf-8')
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
    youtube_url = event['youtube_url']
    
    # Download the audio from YouTube
    audio_file_path = download_youtube_audio(youtube_url)
    
    # Upload the audio file to S3
    s3_uri = upload_to_s3(audio_file_path, os.environ['AUDIO_BUCKET'], 'customer_interview.mp3')
    
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