# KEDA

KEDA is a Kubernetes-based Event Driven Autoscaler. With KEDA, you can drive the scaling of any container in Kubernetes based on the number of events needing to be processed.

KEDA is a single-purpose and lightweight component that can be added into any Kubernetes cluster. KEDA works alongside standard Kubernetes components like the Horizontal Pod Autoscaler and can extend functionality without overwriting or duplication. With KEDA you can explicitly map the apps you want to use event-driven scale, with other apps continuing to function. This makes KEDA a flexible and safe option to run alongside any number of any other Kubernetes applications or frameworks.

## How to Install?

- Install KEDA

``` bash
helm repo add kedacore https://kedacore.github.io/charts
```

``` bash
helm repo update
```

``` bash
helm install keda kedacore/keda --namespace keda --create-namespace
```

# Strimzi

``` bash
helm repo add strimzi https://strimzi.io/charts/
```

``` bash
helm repo update
```

``` bash
helm install strimzi strimzi/strimzi-kafka-operator -n strimzi --create-namespace
```

Deploy you first cluster:

``` bash
kubectl apply -f - << EOF
apiVersion: kafka.strimzi.io/v1beta2
kind: Kafka
metadata:
  name: my-cluster
  namespace: strimzi
spec:
  kafka:
    version: 3.6.1
    replicas: 3
    listeners:
      - name: plain
        port: 9092
        type: internal
        tls: false
      - name: tls
        port: 9093
        type: internal
        tls: true
    config:
      offsets.topic.replication.factor: 3
      transaction.state.log.replication.factor: 3
      transaction.state.log.min.isr: 1
      default.replication.factor: 3
      min.insync.replicas: 1
      inter.broker.protocol.version: "3.3"
    storage:
      type: ephemeral
  zookeeper:
    replicas: 3
    storage:
      type: ephemeral
  entityOperator:
    topicOperator: {}
    userOperator: {}
EOF
```

Deploy a topic:

``` bash
kubectl apply  -f - << EOF
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaTopic
metadata:
  name: samples
  namespace: strimzi
  labels:
    strimzi.io/cluster: my-cluster
spec:
  partitions: 3
  replicas: 1
EOF
```

## Create a dummy prodcer

``` bash
kubectl apply -f - << EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: consumer-dummy
  namespace: default
  labels:
    app: consumer
spec:
  replicas: 1
  selector:
    matchLabels:
      app: consumer
  template:
    metadata:
      labels:
        app: consumer
    spec:
      containers:
      - name: consumer
        image: nginx:1.23.0
EOF
```

``` bash
kubectl apply -f - << EOF
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: kafka-scale-producer
  namespace: default
  labels:
    deploymentName: consumer-dummy
spec:
  scaleTargetRef:
    kind: deployment
    name: consumer-dummy
  pollingInterval: 5
  minReplicaCount: 1
  maxReplicaCount: 10
  triggers:
    - type: kafka
      metadata:
        consumerGroup: my-kafka-consumer-group
        bootstrapServers: my-cluster-kafka-brokers.strimzi.svc.cluster.local:9092
        topic: samples
        lagThreshold: "3"
        offsetRestPolicy: latest
        allowIdleConsumers: "true"
EOF
```

Deploy a producer:

``` bash
kubectl apply -f - << EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kafka-producer
  labels:
    app: kafka-producer
spec:
  replicas: 1
  selector:
    matchLabels:
      app: kafka-producer
  template:
    metadata:
      labels:
        app: kafka-producer
    spec:
      containers:
      - name: kafka-producer
        image: bitnami/kafka:3.1.0
        command:
        - "/bin/sh"
        - "-c"
        - >
          kafka-consumer-groups.sh --bootstrap-server my-cluster-kafka-brokers.strimzi.svc.cluster.local:9092 --group my-kafka-consumer-group --topic samples --execute --reset-offsets --to-earliest;

          while true; do
            echo "YourEventPayload" | kafka-console-producer.sh --topic samples --bootstrap-server my-cluster-kafka-brokers.strimzi.svc.cluster.local:9092 --producer-property linger.ms=1  --producer-property batch.size=65536;
            
            kafka-consumer-groups.sh --bootstrap-server my-cluster-kafka-brokers.strimzi.svc.cluster.local:9092 --group my-kafka-consumer-group --describe;
          done
EOF
```

Create a producer:

``` bash
kubectl run kafka-client --rm -ti --image bitnami/kafka:3.1.0 -n strimzi -- bash
```

Produce Events:

``` bash
kafka-console-producer.sh --topic samples --request-required-acks all --bootstrap-server my-cluster-kafka-brokers.strimzi.svc.cluster.local:9092
```

Consume Events:

``` bash
kafka-console-consumer.sh --topic samples --from-beginning --bootstrap-server my-cluster-kafka-brokers.strimzi.svc.cluster.local:9092
```

Check lag:

``` bash
kafka-run-class.sh kafka.tools.GetOffsetShell --bootstrap-server my-cluster-kafka-brokers.strimzi.svc.cluster.local:9092  --topic samples --time -1
```

``` bash
kafka-consumer-groups.sh --bootstrap-server my-cluster-kafka-brokers.strimzi.svc.cluster.local:9092 --group my-kafka-consumer-group --describe
```

Reset LAG:

``` bash
kafka-consumer-groups.sh --bootstrap-server my-cluster-kafka-brokers.strimzi.svc.cluster.local:9092 --group my-kafka-consumer-group --topic samples --execute --reset-offsets --to-earliest
```

Query KEDA:

``` bash
kubectl get --raw "/apis/external.metrics.k8s.io/v1beta1/namespaces/default/s0-kafka-samples?labelSelector=scaledobject.keda.sh%2Fname%3Dkafka-scale-producer" | jq
```

``` bash
kubectl get --raw "/apis/external.metrics.k8s.io/v1beta1/namespaces/{NAMESPACE}/{METRICS_FROM_CR}}?labelSelector=scaledobject.keda.sh%2Fname%3D{SCALEDOBJECT_NAME}" | jq
```
