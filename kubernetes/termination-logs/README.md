# Termination Logs Workshop!

Here you can find all the resources needed to run the workshop


<br>
<br>

## Run the workshop
1. Apply the base application - [link to code](./apps/step1_simple_app/app.py)
```bash
kubectl apply -f https://raw.githubusercontent.com/guymenahem/how-to-devops-tools/main/kubernetes/termination-logs/step1_simple_app.yaml
```

2. Apply the application that writes error to the termination logs path - [link to code](./apps/step2_write-termination-logs-to-file/app.py)
```bash
kubectl apply -f https://raw.githubusercontent.com/guymenahem/how-to-devops-tools/main/kubernetes/termination-logs/step2_write_termination_logs.yaml
```

3. Make the logs appear in `kubectl describe pod {pod-name}` using configuration only
```bash
kubectl apply -f https://raw.githubusercontent.com/guymenahem/how-to-devops-tools/main/kubernetes/termination-logs/step3_show_error_in_kubectl_describe.yaml
```

4. Demo that k8s exports only errors - [link to code](./apps/step4_extract_only_failed_logs/app.py)
```bash
kubectl apply -f https://raw.githubusercontent.com/guymenahem/how-to-devops-tools/main/kubernetes/termination-logs/step4_auto_filter_info_logs.yaml
```



<br><br>
## Build your images

``` bash
docker buildx build apps/step1_simple_app -t ghcr.io/guymenahem/termination-log-image:0.0.1 --platform=linux/arm64,linux/amd64 --load;

docker buildx build apps/step2_write-termination-logs-to-file -t ghcr.io/guymenahem/termination-log-image:0.0.2 --platform=linux/arm64,linux/amd64 --load;

docker buildx build apps/step4_extract_only_failed_logs -t ghcr.io/guymenahem/termination-log-image:0.0.4 --platform=linux/arm64,linux/amd64 --load;
```