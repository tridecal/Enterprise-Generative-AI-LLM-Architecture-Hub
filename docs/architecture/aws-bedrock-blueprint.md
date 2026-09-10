# Enterprise RAG & Agentic Architecture: AWS Bedrock Stack

## System Architecture Diagram
```mermaid
graph TD
    Client[Enterprise Client / API Consumer] -->|HTTPS REST| APIGW[Amazon API Gateway]
    
    subgraph Ingress & Identity Layer
        APIGW -->|Cognito JWT / IAM| Auth[AWS WAF & Cognito]
    end

    APIGW -->|Routed Payload| LambdaHandler[AWS Lambda / Fargate Agent]

    subgraph AWS Bedrock Orchestration Realm
        LambdaHandler -->|Invoke Agent| BedrockAgent[Amazon Bedrock Agent Core]
        
        subgraph Guardrails & FinOps
            BedrockAgent -->|Enforce Policy| Guardrails[Bedrock Guardrails]
            BedrockAgent -->|Stream Logs| CloudWatch[CloudWatch & AWS X-Ray]
        end

        BedrockAgent -->|Retrieve Query| KB[Bedrock Knowledge Base]
    end

    subgraph Vector & Knowledge Storage
        KB -->|Vector Search| OpenSearch[Amazon OpenSearch Serverless / Aurora pgvector]
        KB -->|Document Sync| S3[Amazon S3 Knowledge Bucket]
    end

    BedrockAgent -->|Inference Call| FM[Foundation Models: Anthropic Claude 3.5 / Bedrock Titan]