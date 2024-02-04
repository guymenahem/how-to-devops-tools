from flask import Flask
from prometheus_client import generate_latest, REGISTRY, Metric, Counter
from flask import Response
import random
import time
import logging

app = Flask(__name__)

class RequestsMetricCollector:
    def collect(self):
        metric = Metric('requests_per_second', 'Requests per Second', 'gauge')
        metric.add_sample('requests_per_second', labels={}, value=random.random() * 100)
        return [metric]

requests_metric_collector = RequestsMetricCollector()
REGISTRY.register(requests_metric_collector)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/metrics')
def metrics():
    return Response(generate_latest(REGISTRY), mimetype='text/plain')

if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0')
