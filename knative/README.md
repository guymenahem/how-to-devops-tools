# Knative

Knative is an Open-Source Enterprise-level
solution to build Serverless and Event Driven Applications

## Deploy Knative Serving

- Install Knative CLI client:

``` bash
brew install knative/client/kn
```

- Install Knative operator

``` bash
kubectl apply -f https://github.com/knative/operator/releases/download/knative-v1.12.1/operator.yaml
```

## Install Knative Serving

```bash
kubectl apply -f knative-serving
```

- Deploy DNS

``` bash
kubectl apply -f https://github.com/knative/serving/releases/download/knative-v1.12.3/serving-default-domain.yaml
```

## Deploy Knative Eventing

``` bash
kubectl apply -f knative-eventing
```

- Deploy Kafka Controller

``` bash
kubectl apply -f https://github.com/knative-extensions/eventing-kafka-broker/releases/download/knative-v1.12.1/eventing-kafka-controller.yaml
```

- Deploy Kakfa Data Plane

``` bash
kubectl apply -f https://github.com/knative-extensions/eventing-kafka-broker/releases/download/knative-v1.12.1/eventing-kafka-source.yaml
```

## Deploy Kafka Topic

- Deploy Strimzi

``` bash
helm install strimzi strimzi/strimzi-kafka-operator -n strimzi --create-namespace
```

- Create Kafka Cluster & Topic

``` bash
kubectl apply -f strimzi-kafka
```

- Wait for the pods to be healthy

## Deploy Knative Service

- Deploy a Knative Service:

``` bash
kubectl apply -f - << EOF
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: event-display
  namespace: default
spec:
  template:
    spec:
      containers:
        - # This corresponds to
          # https://github.com/knative/eventing/tree/main/cmd/event_display/main.go
          image: gcr.io/knative-releases/knative.dev/eventing/cmd/event_display
EOF
```

- Check Service pods

```bash
kubectl get pods
```

- Deploy a knative KafkaSource

``` bash
kubectl apply -f - << EOF
apiVersion: sources.knative.dev/v1beta1
kind: KafkaSource
metadata:
  name: kafka-source
spec:
  consumerGroup: knative-group
  bootstrapServers:
  - my-cluster-kafka-brokers.strimzi.svc.cluster.local:9092
  topics:
  - knative-demo-topic
  sink:
    ref:
      apiVersion: serving.knative.dev/v1
      kind: Service
      name: event-display
EOF
```

- Verify Binding

``` bash
kubectl get kafkasource kafka-source
```

- Create a cloud event in the Kafka Topic

``` bash
kubectl -n strimzi run kafka-producer -ti --image=strimzi/kafka:0.14.0-kafka-2.3.0 --rm=true --restart=Never -- bin/kafka-console-producer.sh --broker-list my-cluster-kafka-brokers.strimzi.svc.cluster.local:9092 --topic knative-demo-topic
```

Write the message in the prompt

- Follow messages recieved by the Knative service

``` bash
kubectl logs --selector='serving.knative.dev/service=event-display' -c user-container -n default -f 
```

If it doesn't exist, create events in the queue and show how the pod is created
