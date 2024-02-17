# K3S / K3D

The certified Kubernetes distribution built for IoT & Edge computing.

This guide is for k3d because I'm using mac machine and k3s required multipass to run so I will use k3d.

## Install k3d

```bash
wget -q -O - https://raw.githubusercontent.com/k3d-io/k3d/main/install.sh | bash
```

## Deploy a cluster

- Deploy you first cluster

```bash
k3d cluster create mycluster
```

- Check the nodes (running on docker)

```bash
docker ps
```

## Deploy an application

- Deploy a deployment

```bash
kubectl apply -f - << EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-nginx
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:latest
        ports:
        - containerPort: 80
EOF
```

- Create a service

```bash
kubectl apply -f - << EOF
apiVersion: v1
kind: Service
metadata:
  name: my-nginx-service
spec:
  selector:
    app: nginx
  ports:
    - protocol: TCP
      port: 8080
      targetPort: 80
  type: LoadBalancer
EOF
```

- Deploy Treafik Ingress

```bash
kubectl apply -f - << EOF
apiVersion: traefik.containo.us/v1alpha1
kind: IngressRoute
metadata:
  name: nginx-ingressroute
spec:
  entryPoints:
    - web
  routes:
    - match: Host(`nginx.local`)
      kind: Rule
      services:
        - name: my-nginx-service
          port: 8080
EOF
```

- Create a k3d port

```bash
k3d cluster create test-ingress -p "8080:8080@loadbalancer" --agents 2
```

- Add record to /etc/hosts

```bash
echo "127.0.0.1 nginx.local" | sudo tee -a /etc/hosts
```

- Open the application

```bash
open http://nginx.local:8080
```
