
# Transcription and Insights Extraction using AWS Step Functions

This project leverages AWS services to create a serverless workflow for extracting transcriptions and insights from YouTube videos. It uses AWS Step Functions to orchestrate the process of downloading audio from YouTube, transcribing the audio, extracting insights, and storing the results. The workflow also sends an email containing the transcription and insights.

## Architecture

![Architecture Diagram](images/architecture_diagram.png)

## Components

### AWS Services Used

- **AWS Step Functions**: Orchestrates the entire workflow.
- **AWS Lambda**: Functions to handle each step of the workflow.
- **Amazon Transcribe**: Transcribes audio to text.
- **Amazon Comprehend**: Extracts insights from the transcribed text.
- **Amazon S3**: Stores the transcription and insights results.
- **Amazon SES**: Sends an email with the transcription and insights.

### Lambda Functions

1. **StartTranscriptionLambda**: Downloads the audio from YouTube and starts the transcription job.
2. **CheckTranscriptionStatusLambda**: Checks the status of the transcription job.
3. **ExtractInsightsLambda**: Extracts insights from the transcribed text.
4. **SaveResultsLambda**: Stores the results in S3 and sends an email with the results.

## Setup

### Prerequisites

- AWS Account
- AWS CLI configured with necessary permissions
- Amazon S3 bucket for storing audio and results
- Amazon SES setup for sending emails
- YouTube URL for testing

### Step 1: Deploy Lambda Functions

Deploy each of the Lambda functions in your AWS account. Ensure you have the necessary IAM roles with the correct permissions for each function.

### Step 2: Create Step Function

Create a Step Function in your AWS account using the following definition:

```json
{
  "Comment": "State machine for transcription and insights extraction",
  "StartAt": "StartTranscription",
  "States": {
    "StartTranscription": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-east-1:YOUR_ACCOUNT_ID:function:StartTranscriptionLambda",
      "Next": "WaitForTranscription",
      "ResultPath": "$.transcription"
    },
    "WaitForTranscription": {
      "Type": "Wait",
      "Seconds": 60,
      "Next": "CheckTranscriptionStatus"
    },
    "CheckTranscriptionStatus": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-east-1:YOUR_ACCOUNT_ID:function:CheckTranscriptionStatusLambda",
      "ResultPath": "$.status",
      "Next": "IsTranscriptionComplete"
    },
    "IsTranscriptionComplete": {
      "Type": "Choice",
      "Choices": [
        {
          "Variable": "$.status",
          "StringEquals": "COMPLETED",
          "Next": "ExtractInsights"
        }
      ],
      "Default": "WaitForTranscription"
    },
    "ExtractInsights": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-east-1:YOUR_ACCOUNT_ID:function:ExtractInsightsLambda",
      "ResultPath": "$.insights",
      "Next": "SaveResults"
    },
    "SaveResults": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-east-1:YOUR_ACCOUNT_ID:function:SaveResultsLambda",
      "End": true
    }
  }
}
```

### Step 3: Configure Environment Variables

Ensure that each Lambda function has the necessary environment variables configured. For example:

- `AUDIO_BUCKET`: S3 bucket for storing audio files.
- `TRANSCRIBE_OUTPUT_BUCKET`: S3 bucket for storing transcription output.
- `RESULTS_BUCKET`: S3 bucket for storing final results.
- `SENDER_EMAIL`: Email address configured in Amazon SES for sending emails.

### Step 4: Test the Workflow

Use the following event JSON to test the `StartTranscriptionLambda` function:

```json
{
  "youtube_url": "YOUR_YOUTUBE_URL",
  "recipient_email": "RECIPIENT_EMAIL"
}
```

### Step 5: Monitor the Workflow

Monitor the Step Function execution in the AWS Management Console to ensure each step completes successfully. Check the logs in CloudWatch for debugging any issues.

## Usage

1. **Start the transcription**: Trigger the `StartTranscriptionLambda` function with the YouTube URL and recipient email.
2. **Check status and get results**: The Step Function will handle checking the status, extracting insights, and saving the results.

## Conclusion

This project demonstrates how to build a serverless workflow using AWS Step Functions, Lambda, Transcribe, Comprehend, S3, and SES to automate the process of extracting insights from YouTube videos. The architecture ensures scalability, cost-efficiency, and ease of management.
