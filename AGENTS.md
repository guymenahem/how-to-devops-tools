# AGENTS.md

## Cursor Cloud specific instructions

### What this repo is
`how-to-devops-tools` is an educational monorepo. Each top-level directory (e.g. `argocd`, `istio`,
`prometheus-grafana`, `kubernetes`, `grpc`, `dapr`, `crossplane`, ...) is a **standalone hands-on
demo** for a specific DevOps / cloud-native tool. It is mostly Kubernetes YAML, Helm values, and
small sample apps (Python/Go/Node). There is **no repo-wide build/lint/test/run command** — pick a
demo directory and follow its own `README.md`.

Pre-installed dev tooling (captured in the VM snapshot): `docker`, `kubectl`, `helm`, `k3d`, plus
`go`, `python3`/`pip3`, and `node`/`npm`. Sample-app Python/Node deps are installed per-demo
(`pip install -r requirements.txt`, `npm install`); Go deps are pre-warmed by the startup update
script.

### Docker must be started manually each session
The Docker daemon is **not** running automatically on a fresh VM. Start it before building images or
running containers:

```bash
sudo dockerd > /tmp/dockerd.log 2>&1 &
```

The daemon is pre-configured in `/etc/docker/daemon.json` to use the `fuse-overlayfs` storage driver
with `containerd-snapshotter` disabled (required for Docker-in-Docker in this VM — do not remove).

### IMPORTANT: local Kubernetes clusters do NOT run in this VM
Do not spend time trying to start a cluster with `k3d` / `kind` / `minikube` — the kubelet fails with
`failed to find memory cgroup (v2)`. The VM's cgroup-v2 root is `domain threaded`, so the `memory`
(and `io`/`hugetlb`) controllers cannot be delegated to child cgroups (`+memory` on
`/sys/fs/cgroup/cgroup.subtree_control` returns `ENOTSUP`). Regular `docker run` works, but
`docker run --memory=...` also fails for the same reason. This is a host/infra limitation, not a
missing dependency.

Consequences for testing demos here:
- You **can** build sample-app images (`docker build`) and run them directly (`docker run -p ...`),
  and run the Go/Python/Node sample apps natively.
- You **cannot** verify `kubectl apply` / `helm install` against a live local cluster in this VM.
  `kubectl` and `helm` are installed and usable as CLIs (e.g. `helm template`, `kubectl --help`,
  chart linting), but there is no API server to deploy to. If a task truly needs a running cluster,
  it must run on infra where cgroup-v2 memory delegation is available.

### Running a sample app (example workflow)
The `prometheus-grafana/sample-app` Flask app is a good smoke test:

```bash
sudo dockerd > /tmp/dockerd.log 2>&1 &        # if not already running
cd prometheus-grafana/sample-app
sudo docker build -t sample-app:dev .
sudo docker run -d --name sample-app -p 8080:8080 sample-app:dev
curl http://localhost:8080/          # -> Hello, World!
curl http://localhost:8080/metrics   # -> Prometheus metrics incl. requests_per_second
```

Native Go example (`buildpacks/go-app`):

```bash
cd buildpacks/go-app
go build -o /tmp/go-app .
PORT=8090 /tmp/go-app &
curl http://localhost:8090/          # -> <h1>Hello World!</h1>
```

Use `sudo` with `docker` (the `ubuntu` user is in the `docker` group, but the group only applies to
new login sessions).
