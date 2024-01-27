#dependencies
import random
import os
from time import sleep    
import requests
import logging
from dapr.clients import DaprClient
from dapr.clients.grpc._state import StateItem
from dapr.clients.grpc._request import TransactionalStateOperation, TransactionOperationType

role = str(os.environ.get('STATE_WOKER_ROLE')).lower()

#code
logging.basicConfig(level = logging.INFO)
DAPR_STORE_NAME = "statestore"

logging.info(f"Starting worker with role: {role}")

if role == 'writer':
    while True:
        sleep(random.randrange(50, 5000) / 1000)
        order = {"id": random.randint(1, 5),
                 "sum": random.randint(1, 50000)}
        with DaprClient() as client:
            #Using Dapr SDK to save and get state
            client.save_state(DAPR_STORE_NAME, "latest_order", str(order)) 
        logging.info(f" Order {order['id']} saved with sum {order['sum']}")

elif role == 'reader':
        while True:
            sleep(random.randrange(50, 5000) / 1000)
            with DaprClient() as client:
                #Using Dapr SDK to save and get state
                result = client.get_state(DAPR_STORE_NAME, "latest_order")
                logging.info(' Order info: ' + result.data.decode('utf-8'))
