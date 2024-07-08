import boto3
import json
import os

s3_client = boto3.client('s3')
ses_client = boto3.client('ses')

def lambda_handler(event, context):
    job_name = event['job_name']
    transcription = event['transcription']
    insights = event['insights']
    recipient_email = event['recipient_email']
    sender_email = os.environ['SENDER_EMAIL']
    
    final_results = {
        'status': 'COMPLETED',
        'transcription': transcription,
        'insights': insights
    }
    
    # Store results in S3
    s3_client.put_object(Bucket=os.environ['RESULTS_BUCKET'], Key=f'results/{job_name}.json', Body=json.dumps(final_results))
    
    # Send results via email
    send_email(job_name, transcription, insights, sender_email, recipient_email)
    
    return {'status': 'COMPLETED', 'insights': insights, 'transcription': transcription, 'job_name': job_name}

def send_email(job_name, transcription, insights, sender_email, recipient_email):
    SUBJECT = f'Transcription and Insights Results for {job_name}'
    
    # Create a formatted insights list
    insights_list = ''.join([f'<li>{insight["Text"]}</li>' for insight in insights])
    
    BODY_HTML = f"""
    <html>
    <head></head>
    <body>
      <h1>Transcription Results for Job {job_name}</h1>
      <p><strong>Transcription:</strong></p>
      <p>{transcription}</p>
      <h2>Insights:</h2>
      <ul>{insights_list}</ul>
    </body>
    </html>
    """
    
    # Provide the contents of the email.
    response = ses_client.send_email(
        Source=sender_email,
        Destination={
            'ToAddresses': [
                recipient_email,
            ]
        },
        Message={
            'Subject': {
                'Data': SUBJECT,
                'Charset': 'UTF-8'
            },
            'Body': {
                'Html': {
                    'Data': BODY_HTML,
                    'Charset': 'UTF-8'
                }
            }
        }
    )

    return response
