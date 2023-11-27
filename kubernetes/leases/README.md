# How to Leases Workshop

## Preps

1. Create a namespace

``` bash
kubectl create ns lease-demo
```

## No Lease

1. Build the service

``` bash
cd 1_no_leases/ &&
docker image build . -f Dockerfile -t no-lease:0.0.1 &&
cd ..
```

1. if using kind - upload images to kind

``` bash
kind load docker-image no-lease:0.0.1 --name local-single-node
```

1. Run the deployment manifests

``` bash
kubectl apply -n lease-demo -f 1_no_leases/deploy
```

1. Check the logs of the container

```bash
kubectl logs -n lease-demo -f -l app=app-lease-example
```

## With Leases

``` bash
cd 2_with_leases &&
docker image build . -f Dockerfile -t with-leases:0.0.1 &&
cd ..
```

1. if using kind - upload images to kind

``` bash
kind load docker-image with-leases:0.0.1 --name local-single-node
```

1. Run the deployment manifests

``` bash
kubectl apply -n lease-demo -f 2_with_leases/deploy
```
