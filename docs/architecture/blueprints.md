# Enterprise AI System Architecture Blueprints

## 1. Enterprise AI Gateway Topology (Kong & LiteLLM Integration)
```mermaid
graph TD
    Client[Enterprise Web / Mobile / Agent Clients] -->|HTTPS / REST| Kong[Kong Enterprise Gateway]
    
    subgraph Edge Security & API Management
        Kong -->|Auth / Global Rate Limits| KongAuth[OAuth2 / mTLS / Key Auth]
        Kong -->|WAF / Traffic Control| KongWAF[Kong WAF & Security Plugins]
    end

    Kong -->|Filtered Traffic| LiteLLM[LiteLLM AI Proxy Gateway]

    subgraph Governance & Observability Engine
        LiteLLM -->|Routing & Failover| Router[Dynamic Model Router]
        LiteLLM -->|Security Check| Guard[NeMo Guardrails / PII Masking]
        LiteLLM -->|FinOps Tracking| Budget[Token & Spend Metering]
        LiteLLM -->|Telemetry| Tracing[OpenTelemetry / LangSmith]
    end

    Router -->|Load Balanced| ProviderA[Azure OpenAI]
    Router -->|Fallback Path| ProviderB[AWS Bedrock]
    Router -->|Self-Hosted| ProviderC[vLLM / Local Cluster]


    ## 2. Multi-Agent Agentic RAG Sequence (CrewAI / LangGraph)

```mermaid
sequenceDiagram
    autonumber
    actor User as Business Client
    participant Gateway as LiteLLM Gateway
    participant Orchestrator as LangGraph Supervisor
    participant AgentRAG as RAG Retrieval Agent
    participant VectorDB as Qdrant Cluster
    participant AgentCritic as Self-Correction Agent

    User->>Gateway: POST /v1/chat/completions (Query)
    Gateway->>Gateway: Check Tokens, Budget & Prompt Guard
    Gateway->>Orchestrator: Dispatch Execution Context
    
    activate Orchestrator
    Orchestrator->>AgentRAG: Assign Task: Retrieve Context
    activate AgentRAG
    AgentRAG->>VectorDB: Query Hybrid Embeddings (Sparse + Dense)
    VectorDB-->>AgentRAG: Return Top-K Passages + Metadata
    AgentRAG-->>Orchestrator: Formulated Context Payload
    deactivate AgentRAG

    Orchestrator->>AgentCritic: Assign Task: Validate Groundedness & Hallucinations
    activate AgentCritic
    alt Context Validated
        AgentCritic-->>Orchestrator: Grounding Score Approved (Score >= 0.85)
    else Context Irrelevant / Hallucinated
        AgentCritic-->>Orchestrator: Flagged Error (Trigger Re-Query)
        Orchestrator->>AgentRAG: Re-try Search with Expanded Scope
    end
    deactivate AgentCritic

    Orchestrator-->>Gateway: Synthesized Final Enterprise Response
    deactivate Orchestrator
    Gateway-->>User: Streaming Response (200 OK)