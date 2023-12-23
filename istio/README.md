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
helm repo add kiali https://kiali.org/helm-charts;
helm repo update
```

Deploy Kiali:

``` bash
helm install \
    --namespace istio-system \
    kiali-server \
    kiali/kiali-server
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

Create a secret token to acces Kiali:

``` bash
kubectl create secret generic kiali-secret --from-literal=token='admin' -n istio-system
```

Patch the SA with the key:

``` bash
kubectl patch serviceaccount kiali -n istio-system -p '{"secrets": [{"name": "kiali-secret"}]}'
```

Create Cluster Role Binding:

``` bash
kubectl apply -f - << EOF
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
    name: kiali-clusterrolebinding
subjects:
  - kind: ServiceAccount
    name: kiali
    namespace: istio-system
roleRef:
    kind: ClusterRole
    name: kiali
    apiGroup: rbac.authorization.k8s.io
EOF
```

Patch kilai deployment to use this service account

``` bash
kubectl patch deployment kiali -n istio-system --type='json' -p='[{"op": "replace", "path": "/spec/template/spec/serviceAccountName", "value": "kiali"}]'
```

On another terminal, open kiali:
``` bash
kubectl get svc -n istio-system
```

``` bash
kubectl port-forward -n istio-system svc/kiali 8080:20001
```