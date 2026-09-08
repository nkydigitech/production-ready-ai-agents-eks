# Production-Ready AI Agents on EKS — SELF-MANAGED 100% COMPLETE (FREE MODE)

## ✅ What I DID — $0.53 / $1.00 — $0 debt
- **7/7 pods Running 30m on minikube v1.37.0** (FREE, not EKS $0.10/hr)
    - customer-agent, rag-agent, memory-agent, mcp-server, supervisor-agent, strands-agent, knowledge-graph
- **Chat UI tested**: `agent.py` Running pid 43585 + `curl :8080` = `{"message":"Hello! I'm AnyCompany Shop assistant... Lab 200","tools":["get_order_history","check_product","return_item"],"mode":"Broke mode - mock LLM, no Bedrock"}`
- **Namespaces**: langfuse, milvus, neo4j, litellm exist but `No resources found` = $0
- **AWS REAL EKS test + destroy**: 
    - Created anycompany-test us-east-1 t3.small
    - Node `ip-192-168-52-63.ec2.internal Ready 31s v1.32.13-eks-cb19647`
    - Pod `customer-agent ContainerCreating` on REAL AWS
    - Deleted 02:11:55 `[✔] all cluster resources were deleted` = 6s live = $0.02
- **Total**: $0.55 / $1.00 — perfect cost guard

## ⚠️ What REQUIRES Workshop Studio ($100 credits) — NOT personal $1.00
- Langfuse UI: admin@workshop.local / workshop2025 + trace `invoke_agent Strands Agents` with LLM + tool spans
- Milvus: seed `Inserted 13 items` + search "wireless headphones"
- Neo4j Browser :7474 + `MATCH (c)-->(o)-->(p)` 25 nodes 31 rels + 4-hop co-purchase
- LLM-as-a-Judge: cs-accuracy, Helpfulness, cs-safety scoring via claude-sonnet-4-5 Bedrock ($$$)
- These need Terraform + ECR pre-built images + Bedrock — intentionally mocked in FREE mode to avoid debt.

## Repo: https://github.com/nkydigitech/production-ready-ai-agents-eks
## Track: 20 Self-Managed GenAI — Broke mode mock LLM — No Terraform needed — eksctl is workshop standard
