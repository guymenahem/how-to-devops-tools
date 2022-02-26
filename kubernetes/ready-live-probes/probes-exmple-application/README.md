# Liveness/Readiness proves example

## How To Run?
1. build the image
   ``` bash
   docker build .  -t ready-live-example:0.0.1
   ```
2. upload the image to the cluster
   ``` bash
   kind load docker-image ready-live-example:0.0.1 --name <clustername>
   ```

3. deploy the application 
   ``` bash
   kubectl apply -f deploy.yaml
   ```

## How To Fail?

This application is based on enviroment variables for failure:
* In order to fail in one of the probes in the current run - change to the enviroment variables of the running container.
In
* In order to fail after the next restart - change the enviroment variables in the deplyoemnt configuration.

</br></br>

### Fail Readiness Probe - Until The Next Restart
This will cause to container to fail in the readiness probe, until the next restart
```bash
kubectl exec $(kubectl get pods -n default -l "app=ready-live-example" -o jsonpath="{.items[0].metadata.name}") -- ./action.sh fail_ready
```
</br>

### Fail Liveness Probe - Until The Next Restart
This will cause to container to fail in the liveness probe, until kubelet will restart it
```bash
kubectl exec $(kubectl get pods -n default -l "app=ready-live-example" -o jsonpath="{.items[0].metadata.name}") -- ./action.sh fail_live
```
</br>

### Succeed Readiness Probe - Until The Next Restart
This will cause to container to fail in the readiness probe, until the next restart
```bash
kubectl exec $(kubectl get pods -n default -l "app=ready-live-example" -o jsonpath="{.items[0].metadata.name}") -- ./action.sh start_ready
```
</br>

### Succeed Liveness Probe - Until The Next Restart
This will cause to container to fail in the liveness probe, until kubelet will restart it
```bash
kubectl exec $(kubectl get pods -n default -l "app=ready-live-example" -o jsonpath="{.items[0].metadata.name}") -- ./action.sh start_live
```
</br>

### Fail Readiness Probe - After The Next Restart
``` bash
kubectl patch deployments.apps ready-live-example --type='json' -p='[{"op": "replace", "path": "/spec/template/spec/containers/0/env/1/value", "value":"True"}]'
```
</br>

### Fail Liveness Probe - After The Next Restart
``` bash
kubectl patch deployments.apps ready-live-example --type='json' -p='[{"op": "replace", "path": "/spec/template/spec/containers/0/env/0/value", "value":"True"}]'
```
</br>

### Make The Container To Restart
``` bash
kubectl delete pod $(kubectl get pods -n default -l "app=ready-live-example" -o jsonpath="{.items[0].metadata.name}")
```
</br>


## How to delete?
``` bash
kubectl delete -f deploy.yaml
```
