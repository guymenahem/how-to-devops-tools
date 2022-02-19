# Metric Server

Metrics Server is a scalable, efficient source of container resource metrics for Kubernetes built-in autoscaling pipelines

### Prerequisites
- A running cluster
- Helm

## How to install the metric server?

### 1. Install the metric server helm chart
add the kubernetes metric server helm repo:
```
​​helm repo add metrics-server https://kubernetes-sigs.github.io/metrics-server/
```

Install the kubernetes dashboard chart:
```
helm upgrade --install metrics-server metrics-server/metrics-server -n metric-server --set 'args={--kubelet-insecure-tls}'
```

### 2. Test your installation
Get the nodes in the cluster:
```
kubctl get nodes
```
Try to access the one of the nodes metric API:
```
kubectl get --raw /apis/metrics.k8s.io/v1beta1/nodes/{NODE-NAME}
```
