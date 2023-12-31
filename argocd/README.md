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

## Deploy Application using ArgoCD

- Optional: Create a new branch

``` bash
git checkout -b argocd
```

- Adjust the yamls to your branch

``` bash
yq --inplace '.spec.source.targetRevision = "argocd"' deploy/apps-definition/frontend-application.yaml
yq --inplace '.spec.source.targetRevision = "argocd"' deploy/apps-definition/backend-application.yaml
yq --inplace '.spec.source.targetRevision = "argocd"' deploy/apps-definition/auth-application.yaml
```

- Deploy ArgoCD App

``` bash
kubectl apply -f deploy/argocd-apps.yaml
```

- Check ArgoCD and review the resources created

## Upgrade image version using ArgoCD

- Change the image of the deployments

``` bash
yq --inplace '.spec.template.spec.containers[0].image = "nginx:1.24.0"' deploy/app-resources/frontend/frontend-deploy.yaml
yq --inplace '.spec.template.spec.containers[0].image = "nginx:1.24.0"' deploy/app-resources/backend/backend-deploy.yaml
yq --inplace '.spec.template.spec.containers[0].image = "nginx:1.24.0"' deploy/app-resources/auth/auth-deploy.yaml
```

- Add changes to git

``` bash
git add deploy/app-resources;
git commit -m "upgrade images" deploy/app-resources;
git push origin argocd
```

- Review the changes in the UI

## Add a new value to the config map

- Change config map

``` bash
yq --inplace '.data.provider= "kubernetes"' deploy/app-resources/backend/backend-cm.yaml
```

- Add changes to git

``` bash
git add deploy/app-resources;
git commit -m "add kubernetes provider" deploy/app-resources/backend/backend-cm.yaml;
git push origin argocd
```

- Review the changes in the UI


## delete the resources

- Delete ArgoCD app

``` bash
kubectl delete -f deploy/argocd-apps.yaml
```

- Delete branch

``` bash
git checkout main;
git branch -D argocd
```
