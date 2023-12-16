# Kyverno

Kyverno (Greek for “govern”) is a policy engine designed specifically for Kubernetes.

## How to Install?

``` bash
helm repo add kyverno https://kyverno.github.io/kyverno/;
helm repo update
```

``` bash
helm install kyverno --namespace kyverno kyverno/kyverno --create-namespace
```

Check Webhooks

``` bash
kubectl get validatingwebhookconfigurations
```

Check Kyverno's CRDs

``` bash
kubectl get crds | grep kyverno
```

## Add Your First Enforce Policy

- Add a policy to block pod creation without requests and limits

``` bash
kubectl apply -f - <<EOF
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-requests-limits
  annotations:
    policies.kyverno.io/title: Require Limits and Requests
    policies.kyverno.io/category: Best Practices, EKS Best Practices
    policies.kyverno.io/severity: medium
    policies.kyverno.io/subject: Pod
    policies.kyverno.io/minversion: 1.6.0
    policies.kyverno.io/description: >-
      As application workloads share cluster resources, it is important to limit resources
      requested and consumed by each Pod. It is recommended to require resource requests and
      limits per Pod, especially for memory and CPU. If a Namespace level request or limit is specified,
      defaults will automatically be applied to each Pod based on the LimitRange configuration.
      This policy validates that all containers have something specified for memory and CPU
      requests and memory limits.      
spec:
  validationFailureAction: Enforce
  background: true
  rules:
  - name: validate-resources
    match:
      any:
      - resources:
          kinds:
          - Pod
    validate:
      message: "CPU and memory resource requests and limits are required."
      pattern:
        spec:
          containers:
          - resources:
              requests:
                memory: "?*"
                cpu: "?*"
              limits:
                memory: "?*"
EOF
```

- Apply a deployment without requests and limits

``` bash
kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
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
        image: nginx:1.23.0
        ports:
        - containerPort: 80
EOF
```

- Add Requests/Limits

``` bash
kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
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
        image: nginx:1.23.0
        ports:
        - containerPort: 80
        resources:
          requests:
            cpu: 1m
            memory: 1Mi
          limits:
            cpu: 100m
            memory: 50Mi
EOF
```

- Delete the policy and deployment

``` bash
kubectl delete clusterpolicy require-requests-limits;
kubectl delete deployments.apps nginx-deployment
```

## Let's add defaults instead of blocking the requests

- Add Mutating Policy

``` bash
kubectl apply -f - <<EOF
apiVersion : kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: add-default-resources
  annotations:
    policies.kyverno.io/title: Add Default Resources
    policies.kyverno.io/category: Other
    policies.kyverno.io/severity: medium
    kyverno.io/kyverno-version: 1.10.0-alpha.2
    policies.kyverno.io/minversion: 1.7.0
    kyverno.io/kubernetes-version: "1.26"
    policies.kyverno.io/subject: Pod
    policies.kyverno.io/description: >-
      Pods which don't specify at least resource requests are assigned a QoS class
      of BestEffort which can hog resources for other Pods on Nodes. At a minimum,
      all Pods should specify resource requests in order to be labeled as the QoS
      class Burstable. This sample mutates any container in a Pod which doesn't
      specify memory or cpu requests to apply some sane defaults.      
spec:
  background: false
  rules:
  - name: add-default-requests
    match:
      any:
      - resources:
          kinds:
          - Pod
    preconditions:
      any:
      - key: "{{request.operation || 'BACKGROUND'}}"
        operator: AnyIn
        value:
        - CREATE
        - UPDATE
    mutate:
      foreach:
      - list: "request.object.spec.containers[]"
        patchStrategicMerge:
          spec:
            containers:
            - (name): "{{element.name}}"
              resources:
                requests:
                  +(memory): "100Mi"
                  +(cpu): "100m"
                limits:
                  +(memory): "100Mi"
                  +(cpu): "100m"
EOF
```

- Deploy a deployment without requests and limits

``` bash
kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-auto-add
  labels:
    app: nginx
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
        image: nginx:1.23.0
        ports:
        - containerPort: 80
EOF
```

- Check the deployment configuration

``` bash
kubectl describe deployments.apps| egrep 'Requests|Limits' -A 2
```

- Delete everything

``` bash
kubectl delete clusterpolicy add-default-resources;
kubectl delete deployments.apps nginx-auto-add
```
