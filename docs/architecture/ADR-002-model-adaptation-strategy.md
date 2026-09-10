# ADR 002: Model Adaptation Strategy (RAG vs. LoRA vs. Full Fine-Tuning)

* **Status**: Accepted
* **Date**: 2026-09-10
* **Deciders**: Principal AI Architect

## Context & Problem Statement
Enterprise applications require domain-specific knowledge adaptation while controlling GPU compute costs, maintaining compliance, and mitigating hallucination risks.

## Decision Matrix

```mermaid
graph TD
    classDef rag fill:#1d3557,stroke:#457b9d,color:#fff;
    classDef lora fill:#2a9d8f,stroke:#264653,color:#fff;
    classDef fineTune fill:#e63946,stroke:#1d3557,color:#fff;

    Requirements[Enterprise Model Adaptation Need] --> KnowledgeType{Is Knowledge Dynamic or Static?}

    KnowledgeType -->|Dynamic / Frequent Updates| RAG["Enterprise RAG Pipeline<br/>• Real-time Data Freshness<br/>• Explicit Traceability & Citations<br/>• Low Compute Overhead"]:::rag

    KnowledgeType -->|Static Domain Rules| DomainScope{Adaptation Scope}

    DomainScope -->|Style, Tone, Output JSON Format| LoRA["LoRA / QLoRA PEFT<br/>• Unsloth Accelerated Tuning<br/>• Specific Domain Syntax<br/>• Moderate Compute Cost"]:::lora

    DomainScope -->|New Base Language / Core Architecture| FullFT["Full Fine-Tuning<br/>• Proprietary Foundation Model<br/>• High Compute Overhead<br/>• Requires C-Level Sign-off"]:::fineTune