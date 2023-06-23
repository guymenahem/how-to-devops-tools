# How To Create KubeConfig For Admins?

### Create Service Account

Create service account for your reomte user:

``` bash
kubectl -n kube-system create serviceaccount cluster-admin-kubeconfig
```

### Create a Secret for the ServiceAccount

```bash
kubectl -n kube-system create  -f - <<EOF
apiVersion: v1
kind: Secret
metadata:
  name: cluster-admin-kubeconfig-token
  annotations:
    kubernetes.io/service-account.name: cluster-admin-kubeconfig
type: kubernetes.io/service-account-token
EOF
```

### Create ClusterRoleBindings

Bind the service account to the cluster-admin cluster role:

``` bash
cat << EOF | kubectl apply -f -
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: cluster-admin-kubeconfig
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: cluster-admin-kubeconfig
  namespace: kube-system
EOF
```

### Build the KubeConfig File

1. Collect kubeconfig variables
``` bash
export USER_TOKEN_VALUE=$(kubectl -n kube-system get secret/cluster-admin-kubeconfig-token -o=go-template='{{.data.token}}' | base64 --decode)
export CURRENT_CONTEXT=$(kubectl config current-context)
export CURRENT_CLUSTER=$(kubectl config view --raw -o=go-template='{{range .contexts}}{{if eq .name "'''${CURRENT_CONTEXT}'''"}}{{ index .context "cluster" }}{{end}}{{end}}')
export CLUSTER_CA=$(kubectl config view --raw -o=go-template='{{range .clusters}}{{if eq .name "'''${CURRENT_CLUSTER}'''"}}"{{with index .cluster "certificate-authority-data" }}{{.}}{{end}}"{{ end }}{{ end }}')
export CLUSTER_SERVER=$(kubectl config view --raw -o=go-template='{{range .clusters}}{{if eq .name "'''${CURRENT_CLUSTER}'''"}}{{ .cluster.server }}{{end}}{{ end }}')
```

2. Collect kubeconfig variables
``` bash
cat << EOF > new-kubeconfig.config
apiVersion: v1
kind: Config
current-context: ${CURRENT_CONTEXT}
contexts:
- name: ${CURRENT_CONTEXT}
  context:
    cluster: ${CURRENT_CONTEXT}
    user: cluster-admin-kubeconfig
    namespace: kube-system
clusters:
- name: ${CURRENT_CONTEXT}
  cluster:
    certificate-authority-data: ${CLUSTER_CA}
    server: ${CLUSTER_SERVER}
users:
- name: cluster-admin-kubeconfig
  user:
    token: ${USER_TOKEN_VALUE}
EOF
```
