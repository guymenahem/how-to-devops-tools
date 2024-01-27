#dependencies
import logging
import random
import os
from time import sleep    
import requests
import logging
import json
from dapr.clients import DaprClient
from dapr.ext.grpc import App, BindingRequest

role = str(os.environ.get('BINDINGS_ROLE')).lower()
logging.basicConfig(level = logging.INFO)
logging.info(f"Starting worker with role: {role}")
BINDING_NAME = 'checkout'
BINDING_OPERATION = 'create' 

if role == 'writer':
    while True:
        sleep(random.randrange(50, 5000) / 1000)
        orderId = random.randint(1, 1000)
        with DaprClient() as client:
            client.invoke_binding(BINDING_NAME, BINDING_OPERATION, json.dumps(orderId))
            logging.info('Sent order for checkout: ' + str(orderId))
        
elif role == 'reader':
    app = App()

    @app.binding('checkout')
    def getCheckout(request: BindingRequest):
        logging.info('Received order for checkout  : ' + request.text())

    logging.info("starting app")
    app.run(6002)
            