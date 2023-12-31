# ArgoCD

Argo CD is a declarative, GitOps continuous delivery tool for Kubernetes.

## Deploy ArgoCD via Helm

- Add ArgoCD Helm Repo

``` bash
helm repo add argo https://argoproj.github.io/argo-helm
```

``` bash
helm repo update
```

- Deploy ArgoCD

``` bash
helm install argocd argo/argo-cd -n argocd --create-namespace --set configs.secret.argocdServerAdminPassword='$2a$12$npJqjPYeo8876hV6mmUL5.7/Mrly/2bBk.P3Uf8a.NGNUu6qkGbNG
' --set configs.secret.argocdServerAdminPasswordMtime="2021-11-08T15:04:05Z"
```

user: admin
password: admin

- Connect to ArgoCD UI

``` bash
open https://127.0.0.1:8080/; kubectl port-forward svc/argocd-server -n argocd 8080:80
```

- Deploy ArgoCD App

``` bash
kubectl apply -f deploy/argocd-apps.yaml
```
 