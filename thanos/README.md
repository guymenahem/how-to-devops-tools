# Thanos

Open source, highly available Prometheus setup with long term storage capabilities.

## Install 2 Promethues clusters

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
```

```bash
helm repo update
```

- Deploy Promethues Operator + Promethues Cluster

```bash
helm upgrade --install prometheus-operator \
  --set prometheus.thanos.create=true \
  --set operator.service.type=ClusterIP \
  --set prometheus.service.type=ClusterIP \
  --set alertmanager.service.type=ClusterIP \
  --set prometheus.thanos.service.type=ClusterIP \
  --set prometheus.externalLabels.cluster="data-producer-prom1" \
  bitnami/kube-prometheus -n prom1 --create-namespace
```

- Deploy Promethues Cluster

```bash
helm upgrade --install prometheus-cluster2 \
  --set operator.enabled=false \
  --set prometheus.serviceAccount.create=false \
  --set prometheus.thanos.create=true \
  --set operator.service.type=ClusterIP \
  --set prometheus.service.type=ClusterIP \
  --set alertmanager.service.type=ClusterIP \
  --set prometheus.thanos.service.type=ClusterIP \
  --set prometheus.externalLabels.cluster="data-producer-prom2" \
  bitnami/kube-prometheus -n prom2 --create-namespace
```

## Deploy Thanos

- Deploy Thanos

```bash
helm upgrade --install thanos bitnami/thanos --values thanos-values.yaml -n thanos --create-namespace
```

- Check reporting in Thanos

```bash
open http://127.0.0.1:9090 ; kubectl port-forward svc/thanos-query -n thanos 9090:9090
```

- Check that the 2 stores are up

## Deploy Grafana

- add Grafana Helm chart

```bash
helm repo add grafana https://grafana.github.io/helm-charts
```

- Deploy Grafana

``` bash
helm upgrade --install grafana grafana/grafana -n grafana --create-namespace \
  -f grafana-values.yaml
```

- Check Grafana Dashboard

user: admin
password: admin

```bash
open http://127.0.0.1:8080; kubectl port-forward svc/grafana -n grafana 8080:80
```

- Check the [data sources](http://127.0.0.1:8080/connections/datasources)

- You can see only one because ut's the thanos global query view

## Query from both Promethues at once

- Go to the [Explore](http://127.0.0.1:8080/explore)

- Run the following [Query](http://127.0.0.1:8080/explore?schemaVersion=1&panes=%7B%229dS%22:%7B%22datasource%22:%22PBFA97CFB590B2093%22,%22queries%22:%5B%7B%22refId%22:%22A%22,%22expr%22:%22sum%20by%28cluster%29%20%28prometheus_http_request_duration_seconds_sum%29%22,%22range%22:true,%22instant%22:true,%22datasource%22:%7B%22type%22:%22prometheus%22,%22uid%22:%22PBFA97CFB590B2093%22%7D,%22editorMode%22:%22code%22,%22legendFormat%22:%22__auto%22,%22useBackend%22:false,%22disableTextWrap%22:false,%22fullMetaSearch%22:false,%22includeNullMetadata%22:true%7D%5D,%22range%22:%7B%22from%22:%22now-30m%22,%22to%22:%22now%22%7D%7D%7D&orgId=1)

``` bash
sum by(cluster) (prometheus_http_request_duration_seconds_sum)
```

- You can also check the number of syncs in Promethues using the [following query](http://127.0.0.1:8080/explore?schemaVersion=1&panes=%7B%229dS%22:%7B%22datasource%22:%22PBFA97CFB590B2093%22,%22queries%22:%5B%7B%22refId%22:%22A%22,%22expr%22:%22sum%20by%28cluster%29%20%28prometheus_operator_node_syncs_total%29%22,%22range%22:true,%22instant%22:true,%22datasource%22:%7B%22type%22:%22prometheus%22,%22uid%22:%22PBFA97CFB590B2093%22%7D,%22editorMode%22:%22builder%22,%22legendFormat%22:%22__auto%22,%22useBackend%22:false,%22disableTextWrap%22:false,%22fullMetaSearch%22:false,%22includeNullMetadata%22:true%7D%5D,%22range%22:%7B%22from%22:%22now-30m%22,%22to%22:%22now%22%7D%7D%7D&orgId=1)

``` bash
sum by(cluster) (prometheus_operator_node_syncs_total)
```
