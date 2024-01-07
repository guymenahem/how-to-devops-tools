# etcd

## Create a single node kind cluster

``` bash
kind create cluster --name local-single-node
```

## Create a etcdclient deployment

``` bash
kubectl apply -f - << EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: etcdclient
  name: etcdclient
spec:
  replicas: 1
  selector:
    matchLabels:
      app: etcdclient
  template:
    metadata:
      labels:
        app: etcdclient
    spec:
      containers:
        - name: etcdclient
          command:
            - sleep
            - 9999d
          image: k8s.gcr.io/etcd:3.3.10
          imagePullPolicy: IfNotPresent
          volumeMounts:
            - mountPath: /etc/kubernetes/pki/etcd
              name: etcd-certs
              readOnly: true
          env:
          - name: ETCDCTL_API
            value: "3"
          - name: ETCDCTL_CACERT
            value: /etc/kubernetes/pki/etcd/ca.crt
          - name: ETCDCTL_CERT
            value: /etc/kubernetes/pki/etcd/healthcheck-client.crt
          - name: ETCDCTL_KEY
            value: /etc/kubernetes/pki/etcd/healthcheck-client.key
          - name: ETCDCTL_ENDPOINTS
            value: "https://127.0.0.1:2379"
      hostNetwork: true
      volumes:
        - name: etcd-certs
          hostPath:
            path: /etc/kubernetes/pki/etcd
            type: DirectoryOrCreate
EOF
```

## Connect to the container

``` bash
kubectl exec $(kubectl get pods --selector app=etcdclient -o jsonpath='{range .items[*]}{.metadata.name}') -it -- /bin/sh
```

## Get the DB strcuture

- Get all keys

``` bash
etcdctl get "" --prefix --keys-only
```

- Get a namespace

``` bash
etcdctl get /registry/namespaces/default -w fields
```

- Get a namespace in json format

``` bash
etcdctl get /registry/namespaces/default -w json
```

## Basic key/value commands

- Save a key

``` bash
etcdctl put test-key 'test-value'
```

- Get the key/value

``` bash
etcdctl get test-key -w fields
```

- Delete the key/value

``` bash
etcdctl del test-key
```

## !!!Warning!!! For Educational Purposes Only

## Create a namespace using etcdctl

``` bash
etcdctl put /registry/namespaces/guy-etcdctl-ns '{"apiVersion":"v1","kind":"Namespace","metadata":{"name":"guy-etcdctl-ns","selfLink":"/api/v1/namespaces/guy-etcdctl-ns","uid":"uid","resourceVersion":"1","creationTimestamp":"2022-10-18T00:00:50Z"}}'
```

``` bash
kubectl get namespace
```

## Create a nginx deployment using etcdctl

``` bash
etcdctl put /registry/deployments/guy-etcdctl-ns/nginx-deployment '{"apiVersion":"apps/v1","kind":"Deployment","metadata":{"name":"nginx-deployment","namespace":"guy-etcdctl-ns","uid":"160422cc-7dae-4762-a81c-7d84ee066e56", "creationTimestamp":"2022-10-18T00:00:50Z"},"spec":{"replicas":3,"selector":{"matchLabels":{"app":"nginx"}},"template":{"metadata":{"labels":{"app":"nginx"}},"spec":{"containers":[{"name":"nginx","image":"nginx:latest","ports":[{"containerPort":80}]}]}}}}'
```

``` bash
kubectl get deploy -n guy-etcdctl-ns
```

## Delete a pod

- Delete a pod

``` bash
kubectl exec $(kubectl get pods --selector app=etcdclient -o jsonpath='{range .items[*]}{.metadata.name}') -it -- etcdctl del /registry/pods/guy-etcdctl-ns/$(kubectl get pods --selector app=nginx -o jsonpath='{range .items[0]}{.metadata.name}' -n guy-etcdctl-ns)
```

- Check the pods controller

``` bash
kubectl get pods -n guy-etcdctl-ns
```
