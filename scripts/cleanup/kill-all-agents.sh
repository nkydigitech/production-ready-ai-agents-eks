#!/bin/bash
echo "Stopping all agents (saves $)..."
kubectl delete namespace anycompany --ignore-not-found
minikube stop
echo "✅ Stopped - AWS cost $0.00, Codespaces paused"
