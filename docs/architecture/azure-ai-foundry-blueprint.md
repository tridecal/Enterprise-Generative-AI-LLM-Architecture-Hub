# Enterprise RAG & Multi-Agent Architecture: Azure AI Foundry Stack

## System Architecture Diagram
```mermaid
graph TD
    Client[Enterprise Application / Teams Bot] -->|HTTPS| AppGateway[Azure Application Gateway + WAF]

    subgraph Identity & Boundary Control
        AppGateway -->|Managed Identity| EntraID[Microsoft Entra ID]
    end

    AppGateway -->|Secure Internal Route| ACA[Azure Container Apps / FastAPI Core]

    subgraph Azure AI Foundry Execution Realm
        ACA -->|Orchestration| AgentService[Azure AI Foundry Agent Service]
        
        subgraph Safety & Observability
            AgentService -->|Content Safety| ContentSafety[Azure AI Content Safety Guardrails]
            AgentService -->|Telemetry| AppInsights[Azure Application Insights]
        end

        AgentService -->|Hybrid Search| AISearch[Azure AI Search Engine]
    end

    subgraph Storage & Vector Subsystem
        AISearch -->|Vector + Keyword Hybrid| Index[HNSW Vector Index & Semantic Ranker]
        Index -->|Source Files| BlobStorage[Azure Blob Storage]
        AgentService -->|Session History| CosmosDB[Azure Cosmos DB]
    end

    AgentService -->|Model Execution| OpenAIModels[Azure OpenAI Service: GPT-4o / O3]