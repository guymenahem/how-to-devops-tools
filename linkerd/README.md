# Linkerd

Linkerd is a service mesh for Kubernetes. It makes running services easier and safer by giving you runtime debugging, observability, reliability, and security—all without requiring any changes to your code.


## Install Linkerd CLI

- Download the CLI

``` bash
curl --proto '=https' --tlsv1.2 -sSfL https://run.linkerd.io/install | sh
```

- Add it to your PATH

``` bash
export PATH=$HOME/.linkerd2/bin:$PATH
```

- Check the CLI is installed

``` bash
linkerd version
```

## Deploy Linkerd

- Verify your Kubernetes cluster

``` bash
linkerd check --pre
```

- Install Linkerd CRDs

``` bash
linkerd install --crds | kubectl apply -f -
```

- Install Linkerd

``` bash
linkerd install | kubectl apply -f -
```

- Check installation

``` bash
linkerd check
```

## Deploy Demo App

- Deploy Emojivoto

``` bash
curl --proto '=https' --tlsv1.2 -sSfL https://run.linkerd.io/emojivoto.yml \
  | kubectl apply -f -
```

- inject a proxy to it by Linkerd

``` bash
kubectl get -n emojivoto deploy -o yaml \
  | linkerd inject - \
  | kubectl apply -f -
```

- Connect to the app

``` bash
kubectl -n emojivoto port-forward svc/web-svc 8080:80
```

## Deploy Linkerd Viz

- Deploy viz

``` bash
linkerd viz install | kubectl apply -f -
```

- Open viz

``` bash
linkerd viz dashboard
```
