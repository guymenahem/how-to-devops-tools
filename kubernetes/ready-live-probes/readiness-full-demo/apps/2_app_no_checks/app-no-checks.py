import os
import logging
import time
from distutils.util import strtobool
from flask import Flask
from flask import make_response

# Initializations
app = Flask("probes-demo")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')


@app.route('/live_check')
def live_check():
    return make_response("OK", 200)


@app.route('/ready_check')
def ready_check():
    logging.info("ready probe check")
    return make_response("OK", 200)


if __name__ == "__main__":
    logging.info("probes demo start")
    app.run(host="0.0.0.0", port=8080)
