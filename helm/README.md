# Helm

The package manager for Kubernetes

## Deploy ArgoCD using Helm

- Add ArgoCD Helm Repo

``` bash
helm repo add argo https://argoproj.github.io/argo-helm
```

``` bash
helm repo update
```

- Check the version available for this chart

``` bash
helm search repo argo --versions
```

- Review the Kubernetes will be created using the chart

``` bash
helm template argocd argo/argo-cd -n argocd --create-namespace --set configs.secret.argocdServerAdminPassword='$2a$12$npJqjPYeo8876hV6mmUL5.7/Mrly/2bBk.P3Uf8a.NGNUu6qkGbNG
' --set configs.secret.argocdServerAdminPasswordMtime="2024-01-01T11:11:11Z" | less
```

- Run a dry run installation of the chart

```bash
helm install argocd argo/argo-cd -n argocd --create-namespace --set configs.secret.argocdServerAdminPassword='$2a$12$npJqjPYeo8876hV6mmUL5.7/Mrly/2bBk.P3Uf8a.NGNUu6qkGbNG
' --set configs.secret.argocdServerAdminPasswordMtime="2024-01-01T11:11:11Z" --dry-run
```

- Deploy ArgoCD

``` bash
helm install argocd argo/argo-cd -n argocd --create-namespace --set configs.secret.argocdServerAdminPassword='$2a$12$npJqjPYeo8876hV6mmUL5.7/Mrly/2bBk.P3Uf8a.NGNUu6qkGbNG
' --set configs.secret.argocdServerAdminPasswordMtime="2024-01-01T11:11:11Z"
```

- Check the chart status

``` bash
helm list -n argocd
```

- Connect to ArgoCD UI

``` bash
open https://127.0.0.1:8080; kubectl port-forward svc/argocd-server -n argocd 8080:80
```

user: admin
password: admin

## Deploy Application using ArgoCD

- Go to the UI and install a chart

- Click on "Create Application" and using the following information

```bash
repo: https://bitnami-labs.github.io/sealed-secrets
chart: sealed-secrets
```

- Review the Chart on using ArgoCD

## Deploy Helm Chart from local

- Review the local chart

- Chart the created resources

``` bash
helm template basic-service ./charts/basic-service/ | less
```

- Deploy it

``` bash
helm install basic-service ./charts/basic-service/
```
