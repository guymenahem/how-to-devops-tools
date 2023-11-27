import os
import logging
import time
import uuid
import socket
from kubernetes import client, config


# Initializations
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')

LEADER_ELECTION_INTERAL = 3

def init_k8s_plugin():
    config.load_kube_config()
    coordinate_client = CoordinationV1Api()
    


def is_master():
    logging.info("I'm the master! hostname: %s", socket.gethostname())
    return True

def run_service():
    logging.info("Starting serving requests as a single instance")
    while True:
        logging.info("Serving requests")
        time.sleep(LEADER_ELECTION_INTERAL)

def start_service():
    while not is_master():
        logging.info("I'm not the master, keep trying")
        time.sleep(LEADER_ELECTION_INTERAL)
    run_service()

if __name__ == "__main__":
    start_service()
