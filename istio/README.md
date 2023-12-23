# Istio

Istio addresses the challenges developers and operators face with a distributed or microservices architecture. Whether you're building from scratch or migrating existing applications to cloud native, Istio can help.

## How to Install?

- add the Helm repo

``` bash
helm repo add istio https://istio-release.storage.googleapis.com/charts;
helm repo update
```

- Install istio-base

``` bash
helm install istio-base istio/base -n istio-system --create-namespace
```

``` bash
helm get all istio-base -n istio-system
```

- Install istiod

``` bash
helm install istiod istio/istiod -n istio-system --wait
```

- Install Kiali

``` bash
kubectl apply -f https://raw.githubusercontent.com/istio/istio/master/samples/addons/kiali.yaml;
kubectl apply -f https://raw.githubusercontent.com/istio/istio/master/samples/addons/prometheus.yaml

```

``` bash
kubectl rollout status deployment/kiali -n istio-system
```

- Deploy bookinfo

[Here is the bookinto app](https://istio.io/latest/docs/examples/bookinfo/)

Enable Injection:

``` bash
kubectl label namespace default istio-injection=enabled
```

Deploy the bookinfo app:

``` bash
kubectl apply -f https://raw.githubusercontent.com/istio/istio/master/samples/bookinfo/platform/kube/bookinfo.yaml
```

Check it's up & running:

``` bash
while true
do
    kubectl exec "$(kubectl get pod -l app=ratings -o jsonpath='{.items[0].metadata.name}')" -c ratings -- curl -sS productpage:9080/productpage | grep -o "<title>.*</title>"
done
```

Inject Faults to the ratings service:

``` bash
kubectl apply -f https://raw.githubusercontent.com/istio/istio/master/samples/bookinfo/networking/virtual-service-ratings-test-abort.yaml
```
