import os
import logging
import time
from distutils.util import strtobool
from flask import Flask
from flask import make_response

# Initializations
app = Flask("probes-demo")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')

if __name__ == "__main__":
    logging.info("probes demo start")
    app.run(host="0.0.0.0", port=8080)
