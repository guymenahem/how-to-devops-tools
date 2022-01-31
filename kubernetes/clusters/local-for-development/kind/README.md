# KIND

Kubernetes in Docker

## how to use
1. install kind

for MacBook:
```
brew install kind
```

2. create the cluster
```
single node cluster:
kind create cluster --name my-single-node-cluster --config kind-single-node-conf.yaml

multi node cluster:
kind create cluster --name my-multi-node-cluster --config kind-multi-node-conf.yaml
```

3. get the nodes
```
kubectl get nodes
```
