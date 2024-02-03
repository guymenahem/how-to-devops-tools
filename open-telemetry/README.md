# OpenTelemetry (OTEL)

OpenTelemetry is an Observability framework and toolkit designed to create and manage telemetry data such as traces, metrics, and logs. Crucially, OpenTelemetry is vendor- and tool-agnostic, meaning that it can be used with a broad variety of Observability backends, including open source tools like Jaeger and Prometheus, as well as commercial offerings.

## Deploy OpenTelemtry Demo

- Add OpenTelemetry Helm Repo

``` bash
helm repo add open-telemetry https://open-telemetry.github.io/opentelemetry-helm-charts; helm repo update
```

- Install OpenTelemetry Demo

```bash
helm install my-otel-demo open-telemetry/opentelemetry-demo
```

- Wait for demo to run (it can take up to 15 minutes)

``` bash
kubectl wait --for=condition=Ready pod -l app.kubernetes.io/name=my-otel-demo-frontendproxy --timeout=15m
```

## Review the demo

- Open port forward

```bash
kubectl port-forward svc/my-otel-demo-frontendproxy 8080:8080
```

- Connect to the systems
  - [Web store](http://localhost:8080/)
  - [Grafana](http://localhost:8080/grafana/)
  - [Feature Flags UI](http://localhost:8080/feature/)
  - [Load Generator UI](http://localhost:8080/loadgen/)
  - [Jaeger UI](http://localhost:8080/jaeger/ui/)

- Go to the app and try to purchase something

- Go to Grafana and check and the collector are reporting

- Go to the load generator and run a test

- Go the feature flag app and enable all 4 flags

- Go back to the app and see that everything is buggy

- Go back to Grafana and check the application dashboard

- Go the jaeger and explore the traces of the ad service & recommendations services
