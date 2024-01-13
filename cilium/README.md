# Cilium

Cilium is an open source, cloud native solution for providing, securing, and observing network connectivity between workloads, fueled by the revolutionary Kernel technology eBPF.

## Deploy a kind cluster without CNI

- Create 3 nodes cluster using the provided configuration

``` bash
kind create cluster --config=kind-cluster-config/cilium-demo-kind-config.yaml --name=cilium-cluster
```

## Install Cilium CLI

- An example for MAC, other architectures can be found [here](https://docs.cilium.io/en/stable/gettingstarted/k8s-install-default/)

``` bash
CILIUM_CLI_VERSION=$(curl -s https://raw.githubusercontent.com/cilium/cilium-cli/main/stable.txt)
CLI_ARCH=amd64
if [ "$(uname -m)" = "arm64" ]; then CLI_ARCH=arm64; fi
curl -L --fail --remote-name-all "https://github.com/cilium/cilium-cli/releases/download/${CILIUM_CLI_VERSION}/cilium-darwin-${CLI_ARCH}.tar.gz{,.sha256sum}"
shasum -a 256 -c cilium-darwin-${CLI_ARCH}.tar.gz.sha256sum
sudo tar xzvfC cilium-darwin-${CLI_ARCH}.tar.gz /usr/local/bin
rm cilium-darwin-${CLI_ARCH}.tar.gz{,.sha256sum}
```

- Install Hubble CLI

``` bash
HUBBLE_VERSION=$(curl -s https://raw.githubusercontent.com/cilium/hubble/master/stable.txt)
HUBBLE_ARCH=amd64
if [ "$(uname -m)" = "arm64" ]; then HUBBLE_ARCH=arm64; fi
curl -L --fail --remote-name-all "https://github.com/cilium/hubble/releases/download/$HUBBLE_VERSION/hubble-darwin-${HUBBLE_ARCH}.tar.gz{,.sha256sum}"
shasum -a 256 -c hubble-darwin-${HUBBLE_ARCH}.tar.gz.sha256sum
sudo tar xzvfC hubble-darwin-${HUBBLE_ARCH}.tar.gz /usr/local/bin
rm hubble-darwin-${HUBBLE_ARCH}.tar.gz{,.sha256sum}
```

- Deploy Cilium

``` bash
helm repo add cilium https://helm.cilium.io/
```

``` bash
helm upgrade --install cilium cilium/cilium --version 1.14.5 \
   --namespace kube-system \
   --set prometheus.enabled=true \
   --set operator.prometheus.enabled=true \
   --set hubble.enabled=true \
   --set hubble.relay.enabled=true \
   --set hubble.ui.enabled=true \
   --set hubble.metrics.enableOpenMetrics=true \
   --set hubble.metrics.enabled="{dns,drop,tcp,flow,port-distribution,icmp,httpV2:exemplars=true;labelsContext=source_ip\,source_namespace\,source_workload\,destination_ip\,destination_namespace\,destination_workload\,traffic_direction}"
```

- Get Cilium Installation Status

``` bash
cilium status
```

- Wait for Cilium to be deployed

``` bash
cilium status --wait
```

## Access using Hubble

- Create a port forward to hubble (on a new windows)

``` bash
cilium hubble port-forward
```

- Check that Hubble can observe traffic

``` bash
hubble observe
```

- Open Hubble UI

``` bash
cilium hubble ui
```

## Deploy Grafana

``` bash
kubectl apply -f https://raw.githubusercontent.com/cilium/cilium/1.14.5/examples/kubernetes/addons/prometheus/monitoring-example.yaml
```

## Deploy example application

- Deploy deathstar application

``` bash
kubectl create -f https://raw.githubusercontent.com/cilium/cilium/1.14.5/examples/minikube/http-sw-app.yaml
```

- Create some traffic

``` bash
kubectl exec xwing -- curl -s -XPOST deathstar.default.svc.cluster.local/v1/request-landing
kubectl exec tiefighter -- curl -s -XPOST deathstar.default.svc.cluster.local/v1/request-landing
```

Both ships, empire & alliance can use the deathstar

- Let's restrict that only empire ships can land on the death star

``` bash
kubectl apply -f - << EOF
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: "rule1"
spec:
  description: "L3-L4 policy to restrict deathstar access to empire ships only"
  endpointSelector:
    matchLabels:
      org: empire
      class: deathstar
  ingress:
  - fromEndpoints:
    - matchLabels:
        org: empire
    toPorts:
    - ports:
      - port: "80"
        protocol: TCP
EOF
```

- Let try to land an tie fighter

``` bash
kubectl exec tiefighter -- curl -s -XPOST deathstar.default.svc.cluster.local/v1/request-landing
```

- And now let's try to land an x-wing

``` bash
kubectl exec xwing -- curl -s -XPOST deathstar.default.svc.cluster.local/v1/request-landing
```

- Check the hubble UI for the drop of information

## Check the Grafana Dahboards

``` bash
open http://127.0.0.1:3000/ && kubectl -n cilium-monitoring port-forward service/grafana --address 0.0.0.0 --address :: 3000:3000
```
