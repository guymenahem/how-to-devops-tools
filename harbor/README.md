# Harbor

Harbor is an open source registry that secures artifacts with policies and role-based access control, ensures images are scanned and free from vulnerabilities, and signs images as trusted. Harbor, a CNCF Graduated project, delivers compliance, performance, and interoperability to help you consistently and securely manage artifacts across cloud native compute platforms like Kubernetes and Docker.

## Deploy Harbor

- Add Helm repo

```bash
helm repo add harbor https://helm.goharbor.io
```

```bash
helm repo update
```

- deploy Harbor

```bash
helm upgrade --install harbor oci://registry-1.docker.io/bitnamicharts/harbor -n harbor --create-namespace \
 --set adminPassword=admin \
 --set service.type=ClusterIP \
 --set externalURL=https://harbor.thegoodguy.io \
 --set ingress.core.hostname=harbor.thegoodguy.io \
 --set nginx.tls.commonName=harbor.thegoodguy.io
```

## Access Harbor

- Create port-forward and access Harbor Dashboard

```bash
open https://127.0.0.1:8443; kubectl port-forward --namespace harbor svc/harbor 8443:443
```

user: admin
password: admin
