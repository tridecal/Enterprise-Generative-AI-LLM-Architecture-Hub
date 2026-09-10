# ADR 001: Selection of Vector Database Strategy (FAISS vs. Qdrant)

* **Status**: Accepted
* **Date**: 2026-09-10
* **Deciders**: Enterprise AI Steering Committee

## Context & Problem Statement
The enterprise AI hub requires a scalable vector indexing solution for high-throughput Retrieval-Augmented Generation (RAG). The platform must support dynamic updates, payload filtering (multi-tenant metadata), and distributed clustering with low latency (<50ms retrieval).

## Decision Drivers
* Dynamic index mutation without full cluster re-indexing.
* Advanced metadata filtering capabilities for multi-tenant isolation.
* Deployment options: Self-hosted Kubernetes vs. managed cloud instances.

## Options Evaluated

| Feature / Capability | Meta FAISS | Qdrant Vector Search Engine |
| :--- | :--- | :--- |
| **Index Type** | In-memory library (HNSW, IVF-PQ) | Native Distributed Service (Rust) |
| **Mutation Support** | Static/Complex index replacement | Dynamic ACID upserts/deletes |
| **Payload Filtering** | Basic numpy/array filtering | Rich JSON metadata key-value filtering |
| **Deployment Mode** | Embedded Python library | Standalone Container / Distributed Cluster |

## Decision Outcome
**Selected Option**: **Qdrant Vector Database** (Production Cloud/Cluster) alongside **FAISS** (Local Sandbox Engine).

### Consequences
* **Positive**: Native payload filtering supports granular document RBAC out of the box.
* **Positive**: Fully dynamic ingestion pipeline eliminates index rebuild downtime.
* **Negative**: Requires separate persistent state management on Kubernetes (Helm/PVs).