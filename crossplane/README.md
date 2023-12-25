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

- Deploy Crossplane with the provider-aws

``` bash
helm install crossplane \
crossplane-stable/crossplane \
--namespace crossplane-system \
--create-namespace \
--set provider.packages='{xpkg.upbound.io/crossplane-contrib/provider-aws:v0.39.0}'
```

## Cofigure AWS Provider

- Create AWS Secret & Key

1 - Create access key using the following [link](https://us-east-1.console.aws.amazon.com/iam/home#/security_credentials/access-key-wizard)

- Create a credentials file

``` bash
tee aws-credentials.txt << EOF
[default]
aws_access_key_id = {Add your access key}
aws_secret_access_key = {Add your secret}
EOF
```

- Create secret based on the json file

``` bash
kubectl create secret \
generic aws-secret \
-n crossplane-system \
--from-file=creds=./aws-credentials.txt
```

- Create Provider Config

``` bash
kubectl apply -f crossplane-config
EOF
```

## Deploy resources on AWS

``` bash
kubectl apply -f aws-resources
```
