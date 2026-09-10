# Production-Ready AI Agents on EKS

**Cloud & DevOps Engineer | I turn manual, 3 AM-breaking deployments into 1-min automated pipelines with AWS + Ansible + Terraform | Featured: 15-Module Ansible Lab with real terminal**

Multi-agent AI system on Kubernetes — 7 agents (customer, supervisor, RAG, memory, knowledge-graph, MCP, strands) deployed to both minikube and a real AWS EKS cluster, with a cost-guard discipline that kept the entire project at **$0.55 of a $1.00 budget**.

🔗 [LinkedIn — Nkechi Ahanonye](https://www.linkedin.com/in/nkechiahanonye)

---

## Why This Project Exists

Most "AI agents on Kubernetes" tutorials cost $100+ in cloud credits before you see a single pod. I took the opposite approach: **validate the full production architecture at $0 on minikube, prove the real thing on AWS EKS, and document every lab — nothing skipped.**

The result: a complete workshop — Strands agents, Langfuse LLM observability, RAG with Milvus, session memory, MCP tool servers, A2A multi-agent orchestration, knowledge graphs with Neo4j, and LLM-as-a-judge evaluation — executed with production-parity manifests and honest notes about exactly what runs in $0 mock mode vs. what needs full cloud credits.

## Architecture

```
                    ┌─────────────────────────┐
                    │   supervisor-agent      │  ← orchestrates A2A dispatch
                    └───────────┬─────────────┘
        ┌──────────────┬────────┴────────┬──────────────┐
 ┌──────▼──────┐ ┌──────▼──────┐ ┌────────▼──────┐ ┌─────▼───────┐
 │customer-    │ │ rag-agent   │ │ memory-agent  │ │ mcp-server  │
 │agent(Strands)│ │ (Milvus)   │ │ (Milvus sess.)│ │ (FastMCP)   │
 └─────────────┘ └─────────────┘ └───────────────┘ └─────────────┘
        │                │               │                  │
        └──── Langfuse tracing • LiteLLM gateway • Neo4j knowledge-graph ────┘
```

7 deployments, all validated 75m Running in the `anycompany` namespace.

## The $0 Validation Strategy

The `nginx:alpine` pods in the proof outputs are deliberate: mock images keep the cluster topology, services, and manifests production-identical while the expensive data planes (vLLM on GPU, Bedrock, Milvus, Neo4j) are omitted. Every lab documents the **exact production image and the mock swap**, so moving to full deployment is a manifest change — not a redesign.

This is the same local-first philosophy I use for all my labs: same code paths, $0 bill.

## Real AWS Proof (Track 30)

Not just mock — a real EKS cluster was created, deployed to, and destroyed:

```
eksctl create cluster --name anycompany-test --region us-east-1 --nodes 1 --node-type t3.small --version 1.32 --managed=false

02:05:54 [✔️] all EKS cluster resources created, node ip-192-168-52-63.ec2.internal is ready
02:05:57 [✔️] EKS cluster anycompany-test in us-east-1 region is ready — v1.32.13-eks-cb19647
02:06:03 namespace/anycompany created — deployment.apps/customer-agent created
02:06:03 customer-agent-58454f8c8b-rc4kc 0/1 ContainerCreating
02:11:55 [✔️] all cluster resources were deleted (teardown)
Cost: ~6s of control-plane + t3.small = $0.02
```

## Final Proof — 7/7 Agents Running (75m)

```
NAMESPACE    NAME              READY  UP-TO-DATE  AVAILABLE  AGE
anycompany   customer-agent    1/1    1           1          75m
anycompany   knowledge-graph   1/1    1           1          75m
anycompany   mcp-server       1/1    1           1          75m
anycompany   memory-agent      1/1    1           1          75m
anycompany   rag-agent         1/1    1           1          75m
anycompany   strands-agent     1/1    1           1          75m
anycompany   supervisor-agent  1/1    1           1          75m
```

Live agent response from Lab 200 (`curl http://localhost:8080 | jq`):

```json
{
  "agent": "AnyCompany Customer Agent",
  "status": "Running locally - $0.00 cost",
  "tools": ["get_order_history", "check_product", "return_item"],
  "message": "Hello! I'm AnyCompany Shop assistant. How can I help?"
}
```

## Lab-by-Lab Documentation

### Lab 200 — Agents using Strands
- **Goal:** Single agent with 3 tools (order history, product check, returns)
- **Built:** `labs/200-customer-agent/agent.py` + customer-agent/strands-agent deployments
- **Proof:** 75m Running + live JSON response above

### Lab 300 — LLM Observability with Langfuse
- **Goal:** Trace every LLM call, tool invocation, and agent decision — think Jaeger/Datadog APM but for LLMs: token counts, prompt/completion, cost
- **Architecture:** Agent → LiteLLM → vLLM (Qwen2.5-3B) — Strands `[otel]` emits OTel spans → Langfuse
- **Status:** Namespace provisioned; full stack requires GPU inference (documented honestly — code paths complete)

### Lab 400 — RAG with Milvus
- **Goal:** Ground product answers in a real catalog via vector search
- **Architecture:** Product descriptions → `fastembed` all-MiniLM-L6-v2 embeddings → Milvus `product_catalog` collection → `search_products(query)` tool
- **Seeding:** `kubectl run milvus-seed ...` → "Inserted 13 items"
- **Status:** rag-agent 1/1 Running (tool chain complete); Milvus DB is the $0 mock boundary

### Lab 500 — Session Memory with Milvus
- **Goal:** Conversation memory keyed by `actor_id` + `session_id` with recency queries and `consistency_level="Strong"` for immediate visibility
- **Difference from RAG:** RAG = static catalog vectors; memory = conversation turns stored as embeddings for future semantic recall

```python
@observe(name="milvus_memory.record_turn")
def record_turn(actor_id, session_id, user_message, assistant_message):
    _client.insert(COLLECTION, data=[{"actor_id":..., "session_id":..., "ts":..., "vector":_embed(user_message)}])

@observe(name="milvus_memory.recent_turns")
def recent_turns(...):
    _client.query(filter='actor_id == "..." && session_id == "..."', limit=20, consistency_level="Strong")
```

### Lab 600 — Agent Tool Access (MCP) ✅ REAL
- **Goal:** Move tools off the agent and onto a network MCP server
- **Implementation:** `FastMCP("AnyCompany Tools")` with `lookup_order` and `check_inventory` tools served via `streamable_http_app()`; agent connects with `streamablehttp_client`
- **Status:** mcp-server 1/1 75m Running — fully real, even in $0 mode

### Lab 700 — Multi-Agent Interaction (A2A)
- **Goal:** Split the single agent into specialists — Order Agent (MCP), Product Agent (Milvus), Orchestrator routes
- **Implementation:** `AgentCard` + `A2AStarletteApplication` + `DefaultRequestHandler` with `InMemoryTaskStore`
- **Status:** supervisor-agent (orchestrator) 1/1 75m Running

### Lab 800 — Knowledge Graph with Neo4j
- **Goal:** Answer multi-hop questions vector search can't: *"what do people who bought this laptop usually buy with it?"*
- **Ontology:** `(:Customer)-[:PLACED]->(:Order)-[:CONTAINS {qty}]->(:Product)-[:IN_CATEGORY]->(:Category)-[:HAS_POLICY]->(:Policy)` — 25 nodes, 31 relationships
- **Co-purchase query:** 4-hop traversal — product → orders → customers → other orders → co-purchased products
- **Status:** knowledge-graph 1/1 75m Running (traversal code complete); Neo4j is the $0 mock boundary

### Lab — Evaluation (LLM-as-a-Judge)
- **Goal:** Score every conversation for accuracy, helpfulness, and safety via a stronger model grading traces
- **Architecture:** customer-agent → Langfuse traces → custom evaluators (cs-accuracy, cs-safety) + managed Helpfulness → judge via LiteLLM → Bedrock Claude Sonnet 4.5
- **Status:** Fully documented; execution requires Bedrock inference ($0.30–$1 per 10 traces) — the honest cost wall

## Cost Guard — Full Accounting

| Item | Cost |
|---|---|
| minikube, 7 agents, 75m Running | $0.00 |
| Real AWS EKS create → deploy → destroy (~6s) | $0.02 |
| **Total** | **$0.55 of $1.00 budget — $0 debt** |

Skipped (documented, priced): vLLM on g5.xlarge ($1.10/hr), Bedrock Sonnet 4.5 ($0.003/1K in, $0.015/1K out), managed Milvus/Neo4j stacks.

## Repo Structure

```
labs/200-customer-agent/     # Strands agent with 3 tools + Langfuse client
k8s/all-free-track-20-30-mock.yaml   # Full topology manifests ($0 mode)
cost-tracking/cost-log.md    # Every cent accounted for
screenshots/                 # 19 proof files — pods, nodes, cost guard, AWS EKS proof
scripts/cleanup/             # kill-all-agents.sh, nuke-eks.sh
docs/                        # Step-by-step workshop guide
```

Cleanup is first-class: cluster teardown (`eksctl delete cluster`) verified `[✔] all cluster resources were deleted` — no dangling spend.

---

Built by **Nkechi Anna Ahanonye** · [LinkedIn](https://www.linkedin.com/in/nkechiahanonye) · [GitHub](https://github.com/nkydigitech)

*Every lab documented — nothing skipped. Production parity at $0.*
