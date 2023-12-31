# FluxCD

Flux is a set of continuous and progressive delivery solutions for Kubernetes that are open and extensible.

## Deploy FluxCD

- Install flux cli

``` bash
brew install fluxcd/tap/flux
```

- Deploy Flux

``` bash
flux install --namespace=flux-system
```

## Create a new branch

``` bash
git checkout -b fluxcd-demo;
git commit -m "empty commit" --allow-empty;
git push origin fluxcd-demo
```

## Deploy using Kustomization

- Add git repo source & Kustomization

``` bash
kubectl apply -f kustomization-demo/flux-config
```

- Add overlay using Kustomize

``` bash
tee -a kustomization-demo/flux-config/kustomizations.yaml << EOF
  patches:
  - op: add
    path: /spec/template/spec/containers/0/image
    value: 1.25.0
EOF
```

- Commit to git

``` bash
git add kustomization-demo/flux-config/kustomizations.yaml;
git commit -m "change image";
git push origin fluxcd-demo
```

## Deploy using Helm

- Add Helm repo

``` bash
kubectl apply -f helm-demo/flux-config
```

## Delete Branch

``` bash
git push origin -d fluxcd-demo;
git checkout main;
git branch -D fluxcd-demo
```
