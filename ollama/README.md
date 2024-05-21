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
  "modelfile": "FROM mistral\nSYSTEM You are data analyst trying to help people to query from their databases. They send you a tables strcture and they want to query and you help them with that. \nPARAMETER temperature 0.2\n"
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
  "prompt": " I have an SQL table with the observability metrics of my services \
              called services_metrics stored in a Postgres database, the columns of the tables are id, timestamp, service_name, mem_usage, cpu_usage.                  
                                          \
              For example: \
              user: 'get me the average memory' answer: 'SELECT AVG(mem) FROM table' \
              user: 'get me the average cpu' answer: 'SELECT AVG(cpu) FROM table' \
              user: 'Write me the SQL query to get my average memory usage of the service aggregator?' \
              Important: Return only the query and nothing more.",
  "stream": false
}' | jq '.response'
```


## Build Chat App

```bash
docker build . -t chat-test:0.0.1
```

```bash
kind load docker-image chat-test:0.0.1 --name single-node-cluster
```

```bash
kubectl apply -f observability-chat/deploy.yaml
```

```bash
kubectl 
```