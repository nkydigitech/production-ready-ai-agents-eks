# 00 — Overview — Self-Managed GenAI Strategy

**Mode**: FREE minikube v1.37.0 — Broke mode
**Cost**: $0.55 / $1.00 — $0 debt
**Date**: 2026-09-08 02:18 UTC

**7 Pods = 7 Labs (core logic deployed)**:
- customer-agent = Lab 200 Agents using Strands
- rag-agent = Lab 400 RAG with Milvus
- memory-agent = Lab 500 Memory Management Milvus
- mcp-server = Lab 600 Agent Tool Access MCP
- supervisor-agent = Lab 700 Multi-Agent A2A Orchestrator
- strands-agent = Lab 200 base
- knowledge-graph = Lab 800 Knowledge Graph Neo4j

**Data planes** (Langfuse, Milvus DB, Neo4j DB, LiteLLM, vLLM) — namespaces exist but `No resources found` = $0 mock. Requires Workshop Studio $100 credits + Terraform + ECR images + Bedrock Claude.

**Repo**: https://github.com/nkydigitech/production-ready-ai-agents-eks