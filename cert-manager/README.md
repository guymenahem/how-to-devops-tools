# Cert-manager

Cloud native certificate management - X.509 certificate management for Kubernetes and OpenShift

## Create kind cluster ready for ingress

```bash
kind create cluster --config=cluster-config/ingress-kind-config.yaml --name=ingress-cluster
```

## Deploy cert-manager

- Add Jetstack repo

```bash
helm repo add jetstack https://charts.jetstack.io
```

- Update Helm Repos

```bash
helm repo update
```

- Deploy cert-manager

```bash
helm upgrade --install cert-manager jetstack/cert-manager --namespace cert-manager \
  --create-namespace --version v1.13.3 --set installCRDs=true
```

## Deploy nginx ingress controller

- Deploy nginx ingress controller

```bash
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx;
helm repo update;
helm upgrade --install global-nginx ingress-nginx/ingress-nginx --set controller.service.type=NodePort --set controller.hostNetwork=true
```

- Check the services

```bash
kubectl get svc
```

- Deploy a simple web application

```bash
helm upgrade --install web-app oci://registry-1.docker.io/bitnamicharts/nginx --set fullnameOverride=web-app --set service.type=ClusterIP
```

- Review the issuer file and apply it

```bash
kubectl apply -f resources/issuer.yaml
```

- Check the issuer created

```bash
kubectl describe issuer self-signed-staging
```

- Create an Ingress for the weba-pp

```bash
kubectl apply -f resources/ingress.yaml
```

- Check the certificate created

```bash
kubectl describe certificates quickstart-example-tls
```

- Check the certificate created

```bash
kubectl describe certificaterequests quickstart-example-tls-1
```

## Check the website

- Create a connection via hostname

```bash
echo "127.0.0.1 thegoodguy.io" | sudo tee -a /etc/hosts
```

- Browse to the website

```bash
open https://example.thegoodguy.io
```

- Save the website certificate

```bash
echo | openssl s_client -servername example.thegoodguy.io -connect example.thegoodguy.io:443 2>/dev/null | openssl x509 
```

- Export certificate from Kubernetes

```bash
kubectl get -o json secret quickstart-example-tls -o jsonpath="{.data}" | jq -r '.["tls.crt"]' | base64 -d
```

- Run diff between them

```bash
diff \
    <(echo | openssl s_client -servername example.thegoodguy.io -connect example.thegoodguy.io:443 2>/dev/null | openssl x509 ) \
    <(kubectl get -o json secret quickstart-example-tls -o jsonpath="{.data}" | jq -r '.["tls.crt"]' | base64 -d)
```
