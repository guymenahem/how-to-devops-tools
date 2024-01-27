# DAPR

Dapr is a portable, event-driven runtime that makes it easy for any developer to build resilient, stateless, and stateful applications that run on the cloud and edge and embraces the diversity of languages and developer frameworks.

## Deploy DAPR

- Install DAPR CLI

```bash
curl -fsSL https://raw.githubusercontent.com/dapr/cli/master/install/install.sh | /bin/bash
```

- Add Helm Repo

``` bash
helm repo add dapr https://dapr.github.io/helm-charts/
```

- Repo update

``` bash
helm repo update
```

- Deploy DAPR

``` bash
helm upgrade --install dapr dapr/dapr --version=1.12 --namespace dapr-system --create-namespace
```

- Deploy DAPR Dashboard

``` bash
helm install dapr-dashboard dapr/dapr-dashboard --namespace dapr-system
```

## State Management

### Deploy Redis

``` bash
helm upgrade --install redis oci://registry-1.docker.io/bitnamicharts/redis --set auth.password="password"
```

## Add Redis as a component to DAPR

``` bash
kubectl apply -f - << EOF
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
spec:
  type: state.redis
  version: v1
  metadata:
  - name: redisHost
    value: redis-master.default.svc.cluster.local:6379
  - name: redisPassword
    value: "password"
  - name: keyPrefix
    value: none
EOF
```

## Build the application

- Build app image

``` bash
cd state-app; docker build . -t dapr-orders-app:0.0.1; cd ..
```

- Load to kind

``` bash
kind load docker-image dapr-orders-app:0.0.1 --name local-single-node
```

- Run application

``` bash
kubectl apply -f state-app/deploy.yaml
```

- Check the logs of both applications at the same time

``` bash
kubectl logs --selector='app=get-orders-app' -c get-orders-app -n default -f
```

```bash
kubectl logs --selector='app=save-orders-app' -c save-orders-app -n default -f
```

- Check DAPR dashboard using port-forwarding

```bash
kubectl port-forward svc/dapr-dashboard -n dapr-system 8080:8080; xdg-open 127.0.0.1:8080
```

## Input & Output bindings

### Deploy Strimzi

``` bash
helm repo add strimzi https://strimzi.io/charts/
```

``` bash
helm repo update
```

``` bash
helm install strimzi strimzi/strimzi-kafka-operator -n strimzi --create-namespace
```

- Deploy you Kafka Cluster

```bash
kubectl apply -f in-out-bindings/kafka.yaml
```

- Create DAPR Kafka Bindings

``` bash
kubectl apply -f in-out-bindings/kafka-bindings.yaml
```

- Build app image

``` bash
cd in-out-bindings; docker build . -t dapr-orders-processing:0.0.1; cd ..
```

- Load to kind

``` bash
kind load docker-image dapr-orders-processing:0.0.1 --name local-single-node
```

- Run application

``` bash
kubectl apply -f in-out-bindings/deploy.yaml
```

- Check Application Logs

``` bash
kubectl logs --selector='app=orders-processor-app' -c get-orders-app -n default -f
```

```bash
kubectl logs --selector='app=orders-generator-app' -c save-orders-app -n default -f
```

- Check DAPR dashboard using port-forwarding

```bash
kubectl port-forward svc/dapr-dashboard -n dapr-system 8080:8080; xdg-open 127.0.0.1:8080
```
