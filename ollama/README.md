# Ollama

## Deploy ollama

```bash
helm repo add ollama-helm https://otwld.github.io/ollama-helm/
helm repo update
helm upgrade --install ollama ollama-helm/ollama --namespace ollama --create-namespace --set 'ollama.models[0]=mistral'
```

## Test the model

- Open port forward

```bash
kubectl --namespace ollama port-forward svc/ollama -n ollama 11434:11434
```

- Generate a simple prompt

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "mistral",
  "prompt": "Why is the sky blue?",
  "stream": false
}'
```

## List all available models

```bash
curl http://localhost:11434/api/tags | jq
```

## Create a new model - only funny things

- Create a new model for SQL purposes

``` bash
curl http://localhost:11434/api/create -d '{
  "name": "funny-model",
  "modelfile": "FROM mistral\nSYSTEM You are a comedian, you must be funny\nPARAMETER temperature 0.2\n"
}'
```

- Query the model

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "funny-model",
  "prompt": "Why is the sky blue?",
  "stream": false
}' | jq '.response'
```

## Create a new model for SQL

- Create a new model for SQL purposes

``` bash
curl http://localhost:11434/api/create -d '{
  "name": "sql-model",
  "modelfile": "FROM mistral\nSYSTEM You are data analyst trying to query data from the DB\nPARAMETER temperature 0.2\nTEMPLATE \"\"\"[INST]{{ if .System }}<<SYS>>{{ .System }}<</SYS>>{{ end }}sql query{{ .Prompt }} [/INST]\"\"\""
}'
```

- Query the model

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "sql-model",
  "prompt": "Why is the sky blue?",
  "stream": false
}' | jq '.response'
```

- Now let's ask a real question

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "sql-model",
  "prompt": "I have an SQL table with obsesrvability metrics of my services. The table name is services_metrics, with the columns id, timestamp, service_name, mem_usage, cpu_usage. What query should I run in SQL to get my average memory usage? In you answer please contain only the sql query",
  "stream": false
}' | jq '.response'
```
