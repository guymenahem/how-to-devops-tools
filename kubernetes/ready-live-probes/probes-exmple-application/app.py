import os
import logging
import time
import signal
from flask import Flask
from flask import make_response

# Initializations
app = Flask("integration-application")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')

liveness_path = "./liveness.pid"
readiness_path = "./readiness.pid"


@app.route('/live')
def live_check():
    if os.path.isfile(liveness_path):
        logging.info("live file found")
        return make_response("OK", 200)
    logging.error("live file not found")
    return make_response("Internal Server Error", 500)


@app.route('/ready')
def ready_check():
    if os.path.isfile(readiness_path):
        logging.info("ready file found")
        return make_response("OK", 200)
    logging.error("ready file not found")
    return make_response("Internal Server Error", 500)


def exit_gracefully(signalNumber, frame):
    logging.critical('Received: %s' % signalNumber)
    return


signal.signal(signal.SIGTERM, exit_gracefully)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
