# Rancher Dashboard

Rancher Dashboard lets you manage clusters and access resources. It has SSO/RBAC capabilities in that platform for teams that don't want to create in-clusters users/roles.

### Prerequisites
- A running cluster
- Helm

## How to install the dashboard?

### 1. Install cert-manager
Add cert-manager CRDs:
``` bash
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.5.1/cert-manager.crds.yaml
```

Add `jetstack` helm repo:
``` bash
helm repo add jetstack https://charts.jetstack.io
```

Install cert-manager:
``` bash
helm install cert-manager jetstack/cert-manager --namespace cert-manager --create-namespace  --version v1.5.1
```

### 2. Install Rancher

Add rancher-stable repo:
``` bash
helm repo add rancher-stable https://releases.rancher.com/server-charts/stable
```

Install Rancher:
``` bash
helm install rancher rancher-stable/rancher --namespace cattle-system --set hostname=rancher.my.org --set bootstrapPassword=admin --set replicas=1  --create-namespace
```

Wait for deployment to rollout:
``` bash
kubectl -n cattle-system rollout status deploy/rancher
```

### 3. Access the dashboard:

Create port-forward:
``` bash
kubectl port-forward -n cattle-system svc/rancher 8080:443
```

The default password should be `admin` but you can get it using this command:
``` bash
kubectl get secrets -n cattle-system bootstrap-secret -o jsonpath='{.data.bootstrapPassword}' | base64 -d
```

Access the dashboard - [https://127.0.0.1:8080](https://127.0.0.1:8080)
