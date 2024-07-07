from diagrams import Diagram, Edge
from diagrams.aws.compute import Lambda
from diagrams.aws.network import APIGateway
from diagrams.aws.storage import S3
from diagrams.aws.compute import Compute

with Diagram("AWS Lambda Function Architecture for Code Generation using Amazon Bedrock", show=False):
    user = APIGateway("User/API Gateway")
    lambda_func = Lambda("Lambda Function")
    bedrock = Compute("Amazon Bedrock")
    s3 = S3("S3 Bucket")

    user >> Edge(label="Invoke") >> lambda_func
    lambda_func >> Edge(label="Invoke Model") >> bedrock
    bedrock >> Edge(label="Return Response") >> lambda_func
    lambda_func >> Edge(label="Save to S3") >> s3
