# Banking Policy Q&A – Local RAG + MCP Demo

Intelligent document Q&A system for banking policies, regulations, and procedures using a Retrieval-Augmented Generation (RAG) pipeline and an MCP-style FastAPI server.

## Architecture

```mermaid
flowchart LR
    A[Streamlit UI] --> B[RAG Pipeline]

    B -->|search_policy / get_section / check_compliance| C[MCP Server]
    C --> B

    subgraph RAG
        B1[Hybrid Retriever<br/>FAISS + BM25]
        B2[Local Cross-Encoder Reranker]
        B3[LLM Answer Generator<br/>GPT-4o-mini]
    end

    subgraph Data
        D1[Text Policies]
        D2[Chunker]
        D3[FAISS Index]
    end
