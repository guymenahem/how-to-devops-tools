# AGENTS.md

## Cursor Cloud specific instructions

### Repository overview

This is a collection of ~30 independent DevOps/Kubernetes tutorial modules (not a unified application). Each top-level directory is a standalone demo with its own README, manifests, and optional sample apps. There is no root-level build, test, or lint command that covers the entire repo.

### Runnable components

| Component | Language | Path | Key commands |
|---|---|---|---|
| Echo Operator | Go 1.21 | `operator-framework/echo-operator/` | `go build -o bin/manager cmd/main.go`, `go vet ./...`, `go fmt ./...` |
| Prometheus sample app | Python (Flask) | `prometheus-grafana/sample-app/` | `python3 app.py` (serves on port 8080) |
| gRPC Node.js client | Node.js | `grpc/demo/node-estimation-client/` | `npm install && node client.js` |
| Various Python demo apps | Python (Flask) | `kubernetes/ready-live-probes/`, `dapr/`, `buildpacks/` | `pip install -r requirements.txt && python3 app.py` |

### Go operator caveats

- The Makefile's `manifests` and `generate` targets use `controller-gen v0.12.0`, which crashes with Go >= 1.22 due to a nil-pointer dereference in `go/types`. Since the generated files (`api/v1/zz_generated.deepcopy.go`, `config/crd/bases/`) are already committed, you can build and test without running those targets.
- To build: `go build -o bin/manager cmd/main.go`
- To test: install `setup-envtest` into `bin/`, then run:
  ```
  KUBEBUILDER_ASSETS="$(./bin/setup-envtest use 1.27.1 --bin-dir $(pwd)/bin -p path)" go test ./... -coverprofile cover.out
  ```

### Python demo apps

Each Python demo app has its own `requirements.txt`. Install with `pip3 install -r requirements.txt` from the app directory. Most apps are Flask-based and serve on port 8080.

### No unified CI or linting

There is no repo-wide linter, test runner, or CI configuration. Lint/test/build commands are per-module as documented in each module's README.
