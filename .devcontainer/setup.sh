#!/bin/bash
set -e
echo "Installing eksctl, kubectl, aws-cli..."

# Install eksctl
if ! command -v eksctl &> /dev/null; then
  curl -sLO "https://github.com/eksctl-io/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz"
  tar -xzf eksctl_$(uname -s)_amd64.tar.gz -C /tmp
  sudo mv /tmp/eksctl /usr/local/bin
  rm eksctl_$(uname -s)_amd64.tar.gz
fi

# Install kubectl
if ! command -v kubectl &> /dev/null; then
  curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
  sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
  rm kubectl
fi

# Install AWS CLI if missing
if ! command -v aws &> /dev/null; then
  curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
  unzip -q awscliv2.zip
  sudo ./aws/install
  rm -rf aws awscliv2.zip
fi

echo "✅ eksctl $(eksctl version)"
echo "✅ kubectl $(kubectl version --client --short 2>&1 || kubectl version --client)"
echo "✅ aws $(aws --version)"
