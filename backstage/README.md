# Backstage

Backstage is an open platform for building developer portals. Powered by a centralized software catalog, Backstage restores order to your microservices and infrastructure and enables your product teams to ship high-quality code quickly — without compromising autonomy.

[Backstage Docs](https://backstage.io/docs/overview/what-is-backstage)

<br>
<br>

## Setup Backstage Development Environment

<br>
<br>

### Set up the repo

1. Fork backstage into your GitHub user [Backstage repo](https://github.com/backstage/backstage)
2. Clone the repo to your local workstation
```
git clone git@github.com:backstage/backstage.git
```
(This is an example from the Backstage repo)

3. cd to the backstage repo

4. Optional - checkout to latest stable version
```
git checkout v1.13.2
```

<br>
<br>

### Install & Configure NVM

NVM - Node Version Manager, nvm allows you to quickly install and use different versions of Node via the command line.

1. Install NVM
```
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash
```
2. Install Node 18
```
nvm install 18
```
3. Use Node version 18
```
nvm use 18
```
4. Set 18 as the default Node version
```
nvm alias default 18
```

<br>
<br>

### Install Yarn
1. Install Yarn
```
npm install --global yarn
```
2. Set Yarn to version 1
```
yarn set version 1.22.19
```
3. Verify the Yarn version
```
yarn --version
```

<br>
<br>

### Create your Backstage Application
1. Create a Backstage application
```
npx @backstage/create-app@latest
```
2. cd to your application directory (based on the given name)
```
cd guy-backstage/
```
3. Run backstage in a development mode
```
yarn dev
```

<br>
<br>

### Verify your application
1. Go to the Backstage UI (should open automatically after the `yarn dev` command)
2. Import a component using this file - `https://github.com/backstage/backstage/blob/master/catalog-info.yaml`
3. Review the example component

<br>
<br>

## Run Backstage On Kubernetes

<br>
<br>

### Build the container image
1. In your application directory, build your application
```
yarn install --frozen-lockfile
yarn tsc
yarn build:backend --config app-config.yaml
```
2. Build the image
```
docker image build . -f packages/backend/Dockerfile --tag backstage:1.0.0
```

<br>
<br>

### Upload the image to your kind cluster

This example is for Kind cluster, you can import the image to your docker repository

```
kind load docker-image backstage:1.0.0 --name local-single-node
```

<br>
<br>

### Deploy Postgres

We're going to use a local Postgres instance, you can use any postgres instance for it.

1. Create the backstage namespace
```
kubectl create ns backstage
```

2. Apply the manifests in the directory from this repo `portgres-resources`. It will create the Postgres resources required with a default username-password.
```
kubectl -f postgres-resources
```

3. Verify the access to Postgres
```
$ kubectl exec -it --namespace=backstage postgres-56c86b8bbc-66pt2 -- /bin/bash
bash-5.1# psql -U $POSTGRES_USER
psql (13.2)
backstage=# \q
bash-5.1# exit
```

<br>
<br>

### Deploy Backstage on Kubernetes

1. Use the Kubernetes instructions on the website - (link)[https://backstage.io/docs/deployment/k8s#creating-the-backstage-instance]



2. Set the Backstage application to use your Postgres DB by adding these environment variables into the backstage deployment.
```
          env:
          - name: POSTGRES_PORT
            value: "5432"
          - name: POSTGRES_HOST
            value: "postgres.backstage.svc.cluster.local"
```

3. Check your running instance by port forwarding to it
```
kubectl port-forward --namespace=backstage svc/backstage 8080:80
```

<br>
<br>

### Deploy the Backstage Kubernetes Plugin
1. Follow the instructions in the documentaion - (link)[https://backstage.io/docs/features/kubernetes/installation]
2. Create a service account in your cluster
```
apiVersion: v1
kind: ServiceAccount
metadata:
  name: backstage-service-account
  namespace: backstage
```
3. Create the cluster role binding
```
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: backstage-cluster-ro
subjects:
- namespace: backstage
  kind: ServiceAccount
  name: backstage-service-account
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: system:aggregate-to-view
```
4. Add the service account to the backstage deployment
```
    spec:
      serviceAccountName: backstage-service-account
```
5. Configure the Kubernetes plugin in backstage by editing the `app-config.yaml`
```
kubernetes:
 serviceLocatorMethod:
   type: 'multiTenant'
 clusterLocatorMethods:
   - type: 'config'
     clusters:
       - url: kubernetes.default.svc.cluster.local:443
         name: local
         authProvider: 'serviceAccount'
         skipTLSVerify: false
         skipMetricsLookup: true
```