#!/bin/bash
set -euo pipefail

docker buildx build -f Dockerfile.sphinxdocs -t registry.sectorfour/meleneth/cnegng-docs:latest --push .
kubectl get pods | grep cnegng-docs | awk '{print $1}' | xargs kubectl delete pod
