# Architectural Diagrams

This folder contains the architectural diagrams for the project.

## Diagram Overview

The diagrams illustrate the high-level architecture and the interaction between different components.

### AWS Lambda Function Architecture for Code Generation using Amazon Bedrock

![Architecture](AWS_Lambda_Function_Architecture_for_Code_Generation_using_Amazon_Bedrock.png)

## Diagram Details

- **User/API Gateway**: Represents users or API Gateway invoking the Lambda function.
- **Lambda Function**: The main function responsible for processing the request and invoking Amazon Bedrock.
- **Amazon Bedrock**: The service used for generating the code based on the provided topic.
- **S3 Bucket**: Where the generated code snippets are stored.

Refer to the main [README](../README.md) for more information about the project.

---

## License

This project is licensed under the MIT License. See the [LICENSE](../LICENSE) file for details.
