# gRPC

In gRPC, a client application can directly call a method on a server application on a different machine as if it were a local object, making it easier for you to create distributed applications and services. As in many RPC systems, gRPC is based around the idea of defining a service, specifying the methods that can be called remotely with their parameters and return types. On the server side, the server implements this interface and runs a gRPC server to handle client calls. On the client side, the client has a stub (referred to as just a client in some languages) that provides the same methods as the server.

## Create the Python Server

- Review the buyingIntent proto file

``` bash
less demo/python-intent-estimation-app/buying_intent.proto
```

- Review the generated code

``` bash
less demo/python-intent-estimation-app/generated_code/buying_intent_pb2_grpc.py
```

- Review the server code

``` bash
less demo/python-intent-estimation-app/server.py
```

- Build the image

``` bash
cd demo/python-intent-estimation-app; docker build -t python-grpc-server:0.0.1 .; cd ../..
```

- Load to kind

```bash
kind load docker-image python-grpc-server:0.0.1 --name local-single-node
```

- Deploy the server

```bash
kubectl apply -f - << EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: python-grpc-server
spec:
  replicas: 1
  selector:
    matchLabels:
      app: python-grpc-server
  template:
    metadata:
      labels:
        app: python-grpc-server
    spec:
      containers:
        - name: grpc-server
          image: python-grpc-server:0.0.1
          ports:
            - containerPort: 8080
---
apiVersion: v1
kind: Service
metadata:
  name: grpc-server-svc
spec:
  selector:
    app: python-grpc-server
  ports:
    - protocol: TCP
      port: 8080
      targetPort: 8080
EOF
```

## Create the Node Client

- Review the client code

``` bash
less demo/node-estimation-client/client.js
```

- Build the image

``` bash
cd demo/node-estimation-client; docker build -t node-grpc-client:0.0.1 .; cd ../..
```

- Load to kind

```bash
kind load docker-image node-grpc-client:0.0.1 --name local-single-node
```

- Deploy the server

```bash
kubectl apply -f - << EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: node-grpc-client
spec:
  replicas: 1
  selector:
    matchLabels:
      app: node-grpc-client
  template:
    metadata:
      labels:
        app: node-grpc-client
    spec:
      containers:
        - name: grpc-client
          image: node-grpc-client:0.0.1
          env:
            - name: TARGET_SERVER
              value: grpc-server-svc.default.svc.cluster.local
EOF
```

## Check the logs

- check server logs

```bash
kubectl logs --selector='app=python-grpc-server' -n default -f
```

- check client logs

```bash
kubectl logs --selector='app=node-grpc-client' -n default -f
```
