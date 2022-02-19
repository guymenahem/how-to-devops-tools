# MiniKube

Minikube is local Kubernetes, focusing on making it easy to learn and develop for Kubernetes.

## Prerequisites
- Docker

## How to create a cluster?

### 1. Download and Install kind
Download and install minikube using this - [link](https://minikube.sigs.k8s.io/docs/start/)

### 2. Create your first cluster - simple
This command will create a cluster with single node.

``` bash
minikube start
```

to test your connection to the cluster use `kubectl get pods`


## MiniKube tricks and tips

### MiniKube dashboard
To open minikube dashboard, use:
``` bash
minikube dashboard
```

### MiniKube expose service
MiniKube let you expose your service locally and open your browser in one command:
``` bash
minikube service {service-name}
```
for example,
``` bash
minikube service my-test-service
```

### Multiple nodes cluster
Set the number of nodes in the start command
``` bash
minikube start --nodes 2
```
