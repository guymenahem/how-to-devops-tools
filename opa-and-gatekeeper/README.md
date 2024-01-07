# Open Policy Agent & Gatekeeper

## Deploy Gatekeeper Helm chart

- Add helm chart

``` bash
helm repo add gatekeeper https://open-policy-agent.github.io/gatekeeper/charts
```

- Install Helm chart

``` bash
helm repo update;
helm install -n gatekeeper-system gatekeeper gatekeeper/gatekeeper --create-namespace
```

## Enforce The Number of Replica

- Apply the contraint template

``` bash
kubectl apply -f - << EOF
apiVersion: templates.gatekeeper.sh/v1
kind: ConstraintTemplate
metadata:
  name: k8sreplicalimits
  annotations:
    metadata.gatekeeper.sh/title: "Replica Limits"
    metadata.gatekeeper.sh/version: 1.0.2
    description: >-
      Requires that objects with the field 'spec.replicas' (Deployments,
      ReplicaSets, etc.) specify a number of replicas within defined ranges.
spec:
  crd:
    spec:
      names:
        kind: K8sReplicaLimits
      validation:
        # Schema for the 'parameters' field
        openAPIV3Schema:
          type: object
          properties:
            ranges:
              type: array
              description: Allowed ranges for numbers of replicas.  Values are inclusive.
              items:
                type: object
                description: A range of allowed replicas.  Values are inclusive.
                properties:
                  min_replicas:
                    description: The minimum number of replicas allowed, inclusive.
                    type: integer
                  max_replicas:
                    description: The maximum number of replicas allowed, inclusive.
                    type: integer
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8sreplicalimits

        object_name = input.review.object.metadata.name
        object_kind = input.review.kind.kind

        violation[{"msg": msg}] {
            spec := input.review.object.spec
            not input_replica_limit(spec)
            msg := sprintf("The provided number of replicas is not allowed for %v: %v. Allowed ranges: %v", [object_kind, object_name, input.parameters])
        }

        input_replica_limit(spec) {
            provided := spec.replicas
            count(input.parameters.ranges) > 0
            range := input.parameters.ranges[_]
            value_within_range(range, provided)
        }

        value_within_range(range, value) {
            range.min_replicas <= value
            range.max_replicas >= value
        }
EOF
```

- Apply the constraint based on the template

``` bash
kubectl apply -f - << EOF
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sReplicaLimits
metadata:
  name: replica-limits
spec:
  match:
    kinds:
      - apiGroups: ["apps"]
        kinds: ["Deployment"]
  parameters:
    ranges:
    - min_replicas: 2
      max_replicas: 10
EOF
```

- Try to deploy a deployment

``` bash
kubectl apply -f - << EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: disallowed-deployment
spec:
  selector:
    matchLabels:
      app: nginx
  replicas: 12
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.24.0
        ports:
        - containerPort: 80
EOF
```

## Enforce Memory requests equals limits

- Add the contraint template

``` bash
kubectl apply -f https://raw.githubusercontent.com/open-policy-agent/gatekeeper-library/master/library/general/containerresourceratios/template.yaml
```

- Add a constraint

``` bash
kubectl apply -f - << EOF
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sContainerRatios
metadata:
  name: container-requests-match-limits
spec:
  match:
    kinds:
      - apiGroups: [""]
        kinds: ["Pod"]
  parameters:
    ratio: "1"
EOF
```

- Try to deploy a deployment

``` bash
kubectl apply -f - << EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: disallowed-deployment2
spec:
  selector:
    matchLabels:
      app: nginx
  replicas: 2
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.24.0
        ports:
        - containerPort: 80
        resources:
            requests:
                memory: 40Mi
            limits:
                memory: 50Mi
EOF
```

- Find the relevant replicaset and check it events
