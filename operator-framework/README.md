# Operator Framework

The Operator Framework is a set of developer tools and Kubernetes components, that aid in Operator development and central management on a multi-tenant cluster.

## Install the operator sdk CLI

- Install the Operator SDK using Brew

```bash
brew install operator-sdk
```

## Create the operator

```bash
mkdir echo-operator
cd echo-operator
operator-sdk init --domain thegoodguy.io --repo github.com/guymenahem/how-to-devops-tools --plugins=go/v4
```

## Define the operator API

```bash
operator-sdk create api --group demo --version v1 --kind EchoServer --resource --controller
```

## Adjust the Echo Spec

- Change the APIs in (api/v1/echoserver_types.go)

``` Go
// EchoServerSpec defines the desired state of EchoServer
type EchoServerSpec struct {
	Message string `json:"message,omitempty"`
}

// EchoServerStatus defines the observed state of EchoServer
type EchoServerStatus struct {
    EchoStatus  string `json:"echoStatus"`
}
```

- Build the manifests

```bash
make manifests
```

## Build the Image

```bash
make docker-build IMG="demo-echo-operator:v0.0.1"
```

## Load the image

```bash
kind load docker-image demo-echo-operator:v0.0.1 --name local-single-node
```

## Deploy the Operator

- Deploy the Echo Operator

```bash
make deploy IMG="demo-echo-operator:v0.0.1"
```

- Check the operator health

```bash
kubectl get pods -n echo-operator-system
```

- Check the operator CRDs

```bash
kubectl get crds
```

- Check the Echos running

```bash
kubectl get echoservers.demo.thegoodguy.io -A
```

## Deploy your first Echo

- Deploy the Echo

```bash
kubectl apply -f - <<EOF
apiVersion: demo.thegoodguy.io/v1
kind: EchoServer
metadata:
  name: my-echo
spec:
  message: "My First Operator in Go!"
  size: 3
EOF
```

- Check the CR

```bash
kubectl describe EchoServer my-echo
```

- Check the Deployment & Service created

```bash
kubectl get deploy -n default
kubectl get svc -n default
```

- Port forward to new server

```bash
kubectl port-forward svc/my-echo-echo-service -n default 8080:8080
```

- On a new windows, run a request to this service

```bash
curl 127.0.0.1:8080
```
