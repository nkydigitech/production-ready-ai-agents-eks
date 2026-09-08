# Production-Ready AI Agents on EKS - FREE Track 20 - One by One

## STEP 0 - Check environment
Command: kubectl get nodes
Expected: minikube Ready
Screenshot: 00-env-check.png

## STEP 1 - Official structure
Command: ls ~/environment/modules/20-self-managed/
Expected: 200-strands-agents 300-observability-langfuse ...
Screenshot: 01-official-structure.png

## STEP 2 - Deploy Lab 200
Command: kubectl create deployment customer-agent --image=nginx:alpine -n anycompany --dry-run=client -o yaml | kubectl apply -f - --validate=false
Expected: deployment.apps/customer-agent created

## STEP 3 - Verify Running
Command: kubectl get pods -n anycompany
Expected: 4 pods Running
Screenshot: 03-lab200-pod-running.png

## STEP 4 - Deploy more FREE
Command: kubectl create deployment rag-agent --image=nginx:alpine -n anycompany --dry-run=client -o yaml | kubectl apply -f - --validate=false
Command: kubectl create deployment memory-agent --image=nginx:alpine -n anycompany --dry-run=client -o yaml | kubectl apply -f - --validate=false
Command: kubectl create deployment mcp-server --image=nginx:alpine -n anycompany --dry-run=client -o yaml | kubectl apply -f - --validate=false

## STEP 5 - Services
Command: kubectl expose deployment customer-agent --port=80 -n anycompany
Command: kubectl get svc -n anycompany
Screenshot: 05-services.png

## STEP 6 - Test local
Command: pkill -f agent.py; python3 labs/200-customer-agent/agent.py & sleep 2; curl -s http://localhost:8080
Expected: AnyCompany Customer Agent $0.00
Screenshot: 06-curl-local.png

## STEP 7 - Cost guard
Command: cat cost-tracking/cost-log.md
Screenshot: 07-cost-guard.png

## STEP 8 - COST WALL Track 30 - DO NOT RUN
Command: ls ~/environment/modules/30-integrated/
Expected: 100-strands-bedrock (costs $$$)
Screenshot: 08-cost-wall.png

## STEP 9 - Delete before debt
Command: kubectl delete namespace anycompany; minikube stop
Screenshot: 09-delete.png
