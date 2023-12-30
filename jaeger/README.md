# Jaeger

Distributed tracing observability platforms, such as Jaeger, are essential for modern software applications that are architected as microservices. Jaeger maps the flow of requests and data as they traverse a distributed system. These requests may make calls to multiple services, which may introduce their own delays or errors. Jaeger connects the dots between these disparate components, helping to identify performance bottlenecks, troubleshoot errors, and improve overall application reliability. Jaeger is 100% open source, cloud native, and infinitely scalable.

## Install Jaeger

``` bash
helm repo add jaegertracing https://jaegertracing.github.io/helm-charts
```

``` bash
helm repo update
```

``` bash
helm install jaeger jaegertracing/jaeger -n jaeger --create-namespace \
  --set allInOne.enabled=true \
  --set provisionDataStore.cassandra=false \
  --set storage.type=none \
  --set agent.enabled=false \
  --set collector.enabled=false \
  --set query.enabled=false
```

## Deploy hotrod

- Deploy hotrod

``` bash
cd hotrod-k8s; 
kustomize build . | kubectl apply -f -;
cd ..
```

- Create port forward to it using port 8080

``` bash
kubectl port-forward -n example-hotrod service/example-hotrod 8080:frontend
```

## Connect to jaeger UI

``` bash
kubectl port-forward -n example-hotrod service/jaeger 8081:frontend
```
