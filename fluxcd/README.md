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

- Check deployed pods

## Deploy new version by updating new image on repo

``` bash
yq --inplace '.spec.template.spec.containers[0].image = "nginx:1.24.0"' kustomization-demo/flux-config/kustomizations.yaml
```

- Commit change to git

``` bash
git add kustomization-demo/flux-config/kustomizations.yaml;
git commit -m "change image 2";
git push origin fluxcd-demo
```

- Check deployed pods

## Deploy new version by overlay kustomization

- Add overlay using Kustomize

``` bash
tee -a kustomization-demo/flux-config/kustomizations.yaml << EOF
  patches:
    - patch: |
        - op: add
          path: /spec/template/spec/containers/0/image
          value: nginx:1.25.0
      target:
        kind: Deployment
        name: demo-application
        namespace: default
EOF
```

- Commit to git

``` bash
git add kustomization-demo/flux-config/kustomizations.yaml;
git commit -m "change image 2";
git push origin fluxcd-demo
```

- Apply the configuration

``` bash
kubectl apply -f kustomization-demo/flux-config
```

## Deploy Helm release using the Helm controller

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
