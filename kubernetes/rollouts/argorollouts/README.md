# ArgoRollouts

## How to install?
1. install argo rollouts using yamls
```
kubectl create namespace argo-rollouts
kubectl apply -n argo-rollouts -f https://github.com/argoproj/argo-rollouts/releases/latest/download/install.yaml
```


2. install your first rollout
```
kubectl apply -f https://raw.githubusercontent.com/argoproj/argo-rollouts/master/docs/getting-started/basic/rollout.yaml
kubectl apply -f https://raw.githubusercontent.com/argoproj/argo-rollouts/master/docs/getting-started/basic/service.yaml
```


3. track the watch
```
kubectl argo rollouts get rollout rollouts-demo --watch
```


