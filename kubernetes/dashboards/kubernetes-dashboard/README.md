# Kubernetes Dashboard

Kubernetes Dashboard is a general purpose, web-based UI for Kubernetes clusters. It allows users to manage applications running in the cluster and troubleshoot them, as well as manage the cluster itself.

### Prerequisites
- A running cluster
- Helm

## How to install the dashboard?

### 1. Install the Kubernetes dashboard helm chart
add the kubernetes-dashboard helm repo:
```
helm repo add kubernetes-dashboard https://kubernetes.github.io/dashboard/
```

Install the kubernetes dashboard helm chart:
```
helm upgrade --install k8s-dashboard kubernetes-dashboard/kubernetes-dashboard -n kubernetes-dashboard --set serviceAccount.create=true --set serviceAccount.name=k8s-dashboard-admin-user --create-namespace
```

### 3. Create the role binding
This rolebinding is neccesery in order to let the dashboard access the API with admin permissions.
``` bash
cat<<EOF|kubectl apply -f -
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: k8s-dashboard-admin-user
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: k8s-dashboard-admin-user
  namespace: kubernetes-dashboard
EOF
```

### 4. Get the Web UI access token 
Can the access token, you will need it to login to the dashboard UI
```
kubectl -n kubernetes-dashboard get secret $(kubectl -n kubernetes-dashboard get sa/k8s-dashboard-admin-user -o jsonpath="{.secrets[0].name}") -o go-template="{{.data.token | base64decode}}"
```

### 5. Create the tunnel to access the UI
Use `kubectl port-forward` to access the dashboard
```
kubectl -n kubernetes-dashboard port-forward $(kubectl get pods -n kubernetes-dashboard -l "app.kubernetes.io/name=kubernetes-dashboard,app.kubernetes.io/instance=k8s-dashboard" -o jsonpath="{.items[0].metadata.name}") 8443:8443
```

### 6. Access the dashboard
Go to the [Kubernetes dashboard](https://127.0.0.1:8443/) and use the token to login.


##### - If you got problem to access using Google Chrome, make sure insecure connection to the localhost is allowed [in the chrome configuration page](chrome://flags/#allow-insecure-localhost)

## Add the metrics server
Add to helm chart install command, the value to enable the metrics scraper:
```
helm upgrade --install ... metricsScraper.enabled=true
```
