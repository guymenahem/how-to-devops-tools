# Prometheus & Grafana

Prometheus and Grafana are popular open-source tools used for monitoring and visualization in the field of IT and software development.

## Deploy Promethues

- Add Prometheus repo

``` bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
```

- Update repo

```bash
helm repo update
```

- Deploy Promethues

```bash
helm upgrade --install prometheus prometheus-community/prometheus -n observability --create-namespace
```

## Deploy Grafana

- Add Grafana repo

``` bash
helm repo add grafana https://grafana.github.io/helm-charts
```

- Update repo

```bash
helm repo update
```

- Deploy Grafana

```bash
helm upgrade --install grafana grafana/grafana -f helm-values/grafana-values.yaml -n observability --create-namespace
```

## Access Grafana

- access grafana using the following credentials(user: admin, password: admin)

```bash
open http://127.0.0.1:8080; kubectl port-forward svc/grafana -n observability 8080:80
```


## Deploy Your Application And Create a Dashboard For It

- Build the image

``` bash
cd sample-app; docker build -t prometheus-sample-app:0.0.1 .; cd ..
```

- Load to kind

```bash
kind load docker-image prometheus-sample-app:0.0.1 --name local-single-node
```

- Deploy the app

```bash
kubectl apply -f - << EOF 
apiVersion: apps/v1
kind: Deployment
metadata:
  name: prometheus-sample-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: prometheus-sample-app
  template:
    metadata:
      labels:
        app: prometheus-sample-app
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/path: /metrics
        prometheus.io/port: "8080"
    spec:
      containers:
      - name: prometheus-sample-app
        image: prometheus-sample-app:0.0.1
        ports:
        - containerPort: 8080
---
apiVersion: v1
kind: Service
metadata:
  name: sample-app
spec:
  selector:
    app: prometheus-sample-app
  ports:
    - name: http
      protocol: TCP
      port: 8080
      targetPort: 8080
EOF
```

## Check that Promethues scrapes your app

- Open the target dashbaord and check there you app is reporting

```bash
open http://127.0.0.1:9090/targets ; kubectl port-forward svc/prometheus-server -n observability 9090:80
```

## Create a dashboard in Grafana

- Open the target dashbaord and check there you app is reporting

```bash
open http://127.0.0.1:8080 ; kubectl port-forward svc/grafana -n observability 8080:80
```

- Import a dashboard

```bash
Dashboards -> Import -> Using ID
ID: 8171
```

- Create a dashboard using the following query

```bash
Dashboards -> New -> New Dashboard -> Add Visualization
```

- Add a chart to the dashboard

Select Promethues as the data source
Change the query builder to code and paste the following query

```bash
requests_per_second{app="prometheus-sample-app"}
```
