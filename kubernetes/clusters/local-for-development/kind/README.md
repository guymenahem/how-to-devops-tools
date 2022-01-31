# Kind

kind is a tool for running local Kubernetes clusters using Docker container “nodes”

## How to create a cluster?

### 1. Install kind
``` bash
# mac users:
brew install kind
```
``` bash
# Windows users:
choco install kind
```
or using this link - [link](https://kind.sigs.k8s.io/docs/user/quick-start/)

### 2. Create your first cluster - simple
This command will create a cluster with single node.

``` bash
kind create cluster
```

to test your connection to the cluster use `kubectl get pods`


### 3. Create your cluster - multi node
To create more complex cluster, using the files:
- [single node cluster configuration](../kind/kind-single-node-conf.yaml)
- [multi node cluster configuration](../kind/kind-multi-node-conf.yaml)
``` bash
kind create cluster --name <cluster-name> --config <config file>
```
for example:
``` bash
kind create cluster --name my-multi-node-cluster --config kind-multi-node-conf.yaml
```