# ArgoRollouts

Advanced Kubernetes deployment strategies such as Canary and Blue-Green made easy.

## Install Argo kuebctl plugin

- Install the plugin

```bash
brew install argoproj/tap/kubectl-argo-rollouts
```

## Deploy ArgoRollouts

```bash
helm repo add argo https://argoproj.github.io/argo-helm;
helm repo update;
helm install argo-rollouts argo/argo-rollouts -n argo-rollouts --create-namespace
```

## Deploy a Canary Rollout

- Deploy the rollout

```bash
kubectl apply -f - << EOF
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: canary-demo
spec:
  replicas: 5
  strategy:
    canary:
      steps:
      - setWeight: 5
      - pause: {}
      - setWeight: 20
      - pause: {duration: 10}
      - setWeight: 60
      - pause: {duration: 10}
      - setWeight: 80
      - pause: {duration: 10}
  revisionHistoryLimit: 2
  selector:
    matchLabels:
      app: canary-demo
  template:
    metadata:
      labels:
        app: canary-demo
    spec:
      containers:
      - name: rollouts-demo
        image: nginx:1.23.0
        ports:
        - name: http
          containerPort: 8080
          protocol: TCP
---
apiVersion: v1
kind: Service
metadata:
  name: canary-demo
spec:
  ports:
  - port: 80
    targetPort: 8080
    protocol: TCP
    name: http
  selector:
    app: canary-demo
EOF
```

- Watch hte rollout using the CLI

```bash
kubectl argo rollouts get rollout canary-demo --watch
```

- Trigger a rollout

```bash
kubectl argo rollouts set image canary-demo rollouts-demo=nginx:1.24.0
```

- Watch the rollout using the CLI

```bash
kubectl argo rollouts get rollout canary-demo --watch
```

- The rollout is in pause, waiting for us to promote it

- Promote the rollout

```bash
kubectl argo rollouts promote canary-demo
```

- Watch the rollout using the CLI

```bash
kubectl argo rollouts get rollout canary-demo --watch
```

## Deploy a Blue/Green Rollout

- Deploy a blue/green rollout

```bash
kubectl apply -f - << EOF
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: bluegreen-demo
spec:
  replicas: 2
  selector:
    matchLabels:
      app: bluegreen-demo
  template:
    metadata:
      labels:
        app: bluegreen-demo
    spec:
      containers:
      - name: bluegreen-demo
        image: nginx:1.23.0
        ports:
        - containerPort: 8080
  strategy:
    blueGreen: 
      activeService: bluegreen-active-demo
      previewService: bluegreen-preview-demo
      autoPromotionEnabled: false
      scaleDownDelaySeconds: 30
---
apiVersion: v1
kind: Service
metadata:
  name: bluegreen-active-demo
spec:
  ports:
  - port: 80
    targetPort: 8080
    protocol: TCP
    name: http
  selector:
    app: bluegreen-demo
---
apiVersion: v1
kind: Service
metadata:
  name: bluegreen-preview-demo
spec:
  ports:
  - port: 80
    targetPort: 8080
    protocol: TCP
    name: http
  selector:
    app: bluegreen-demo
EOF
```

- Watch the rollout using the CLI

```bash
kubectl argo rollouts get rollout bluegreen-demo --watch
```

- Trigger a rollout

```bash
kubectl argo rollouts set image bluegreen-demo bluegreen-demo=nginx:1.24.0
```

- Watch the rollout using the CLI

```bash
kubectl argo rollouts get rollout bluegreen-demo --watch
```

- The rollout is waiting for our approval

- Promote the rollout

```bash
kubectl argo rollouts promote bluegreen-demo
```

- Watch the rollout using the CLI

```bash
kubectl argo rollouts get rollout canary-demo --watch
```

- The pod will remain for 30 second for rollback

- After the rollout is done, lets rollback

- Trigger a rollout

```bash
kubectl argo rollouts set image bluegreen-demo bluegreen-demo=nginx:1.25.0
```

- Promote the rollout

```bash
kubectl argo rollouts promote bluegreen-demo
```

- Watch the rollout using the CLI

```bash
kubectl argo rollouts get rollout bluegreen-demo --watch
```

- Trigger a rollout

```bash
kubectl argo rollouts set image bluegreen-demo bluegreen-demo=nginx:1.24.0
```

## Cleanup

```bash
kubectl delete rollout bluegreen-demo canary-demo
kubectl delete svc bluegreen-active-demo bluegreen-preview-demo canary-demo
```