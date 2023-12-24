# Crossplane

Build control planes without needing to write code. Crossplane has a highly extensible backend that enables you to orchestrate applications and infrastructure no matter where they run, and a highly configurable frontend that lets you define the declarative API it offers.

## How to Install?

- Install Crossplane

``` bash
helm repo add crossplane-stable https://charts.crossplane.io/stable
```

``` bash
helm repo update
```

``` bash
helm install crossplane \
--namespace crossplane-system \
--create-namespace crossplane-stable/crossplane 
```

## Deploy GCP Provider

- Deploy GCP Provider

``` bash
kubectl apply -f - << EOF
apiVersion: pkg.crossplane.io/v1
kind: Provider
metadata:
  name: provider-gcp
spec:
  package: xpkg.upbound.io/crossplane-contrib/provider-gcp:v0.22.0
EOF
```

- Create GCP Service Account

1 - [Create GCP Service account](https://console.cloud.google.com/iam-admin/serviceaccounts/create)
2 - Pick Role as Kubernetes Engine Admin
3 - Create the Service Account
4 - Go to the Service Account Keys
5 - Create a Key
6 - Download the json file

- Change the name of the json key file

``` bash
mv project-name-generated-name.json gcp-credentials.json
```

- Create secret based on the json file

``` bash
kubectl create secret \
generic gcp-secret \
-n crossplane-system \
--from-file=creds=./gcp-credentials.json
```

- Get your GCP project ID

``` bash
export GCP_PROJECT_ID=$(jq -r '.project_id' gcp-credentials.json)
```

- Create Provider Config

``` bash
kubectl apply -f - << EOF
apiVersion: gcp.crossplane.io/v1beta1
kind: ProviderConfig
metadata:
  name: default
spec:
  projectID: $GCP_PROJECT_ID
  credentials:
    source: Secret
    secretRef:
      namespace: crossplane-system
      name: gcp-secret
      key: creds
EOF
```

- Deploy GKE Cluster

``` bash
kubectl apply -f - << EOF
apiVersion: container.gcp.crossplane.io/v1beta2
kind: Cluster
metadata:
  name: crossplane-managed-cluster
spec:
  forProvider:
    location: us-central1
    autopilot:
      enabled: true
  writeConnectionSecretToRef:
    name: auto-kube
    namespace: default
EOF
```
