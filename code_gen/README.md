# AWS Lambda Function for Code Generation using Amazon Bedrock

This repository contains a Python-based AWS Lambda function that generates Python code snippets using the Amazon Bedrock service and saves the generated code to an S3 bucket. The function is triggered via an API Gateway endpoint, making it easy to integrate with various applications and services.

## Features

- **Code Generation**: Generates Python code snippets based on a given topic using Amazon Bedrock.
- **AWS Integration**: Utilizes AWS services such as Lambda, Bedrock, and S3.
- **Serverless Architecture**: Leverages the benefits of a serverless architecture for scalability and cost-efficiency.

## Architecture

![Architecture](path/to/your/architecture-image.png)

## Prerequisites

- AWS account
- IAM role with necessary permissions
- S3 bucket
- Amazon Bedrock setup
- API Gateway setup

Step 3: Deploy the Lambda function
Deploy the Lambda function using the AWS Management Console or AWS CLI.

Step 4: Set up API Gateway
Create an API Gateway endpoint to trigger the Lambda function. You can use the following configuration:

Method: POST
Endpoint: /generate-code
Integration: Lambda Function
Step 5: Update IAM Role
Ensure that your Lambda function's IAM role has the necessary permissions:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel"
            ],
            "Resource": [
                "arn:aws:bedrock:us-east-1::foundation-model/meta.llama3-70b-instruct-v1:0"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject"
            ],
            "Resource": [
                "arn:aws:s3:::your-s3-bucket-name/*"
            ]
        }
    ]
}

```

Usage
API Request
You can test the API using Postman or any other API testing tool. Here is an example request:

URL: https://your-api-gateway-endpoint/generate-code
Method: POST
Body:

```
{
  "codetopic": "sorting algorithms in Python"
}
```

Response
The response will indicate whether the code generation and saving process was successful:

```
{
  "statusCode": 200,
  "body": "Blog Generation is completed"
}
```

Screenshots
![Postman Request](images/postman.png)

![S3 Bucket](images/s3.png)