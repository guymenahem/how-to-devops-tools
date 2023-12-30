# CoreDNS

A DNS server, written in GO. Built using Plugin that allows custom DNS configuration.

## Check resolution

- Deploy a utils pod

``` bash
kubectl apply -f utils
```

- Shell into the pod

``` bash
kubectl exec $(kubectl get pods --selector app=utils -o jsonpath='{range .items[*]}{.metadata.name}') -it -- /bin/sh
```

- Run curl command to kubernetes api using the guy.local address

``` bash
dig google.com +short +identify
dig kubernetes.default.svc.cluster.local +short +identify
dig kubernetes.default.svc.guy.test +short +identify
```

## Adjust Plugins

- Remove the promethues plugin and add guy.test to be resolved

``` bash
kubectl apply -f - << EOF
apiVersion: v1
kind: ConfigMap
metadata:
  name: coredns
  namespace: kube-system
data:
  Corefile: |
    .:53 {
        errors
        health {
           lameduck 5s
        }
        ready
        kubernetes guy.test cluster.local in-addr.arpa ip6.arpa {
           pods insecure
           fallthrough in-addr.arpa ip6.arpa
           ttl 30
        }
        forward . /etc/resolv.conf {
           max_concurrent 1000
        }
        cache 30
        loop
        reload
        loadbalance
    }
EOF
```

- Rollout the coredns deployment

``` bash
kubectl rollout restart deployment -n kube-system coredns
```

- Recheck resolution of kubernetes api using the guy.local address

``` bash
dig kubernetes.default.svc.guy.test +short +identify
```

## Add the Promethues Plugin

- Deploy promethues

``` bash
helm install promethues prometheus-community/kube-prometheus-stack -n promethues --create-namespace
```

- Login to grafana

``` bash
open "http://127.0.0.1:8080/"; kubectl port-forward svc/promethues-grafana -n promethues 8080:80
```

username: admin
password: prom-operator

- Add Promethues plugin

``` bash
kubectl apply -f - << EOF
apiVersion: v1
kind: ConfigMap
metadata:
  name: coredns
  namespace: kube-system
data:
  Corefile: |
    .:53 {
        errors
        health {
           lameduck 5s
        }
        ready
        kubernetes guy.test cluster.local in-addr.arpa ip6.arpa {
           pods insecure
           fallthrough in-addr.arpa ip6.arpa
           ttl 30
        }
        prometheus :9153
        forward . /etc/resolv.conf {
           max_concurrent 1000
        }
        cache 30
        loop
        reload
        loadbalance
    }
EOF
```

- Wait for 5 minutes and check the metrics
