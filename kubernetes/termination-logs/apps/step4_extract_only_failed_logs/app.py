import logging
import traceback

# Initializations
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')

try:
    logging.info("start service")
    raise Exception("unauthorized operation")
except Exception as e:
    logging.exception(e)
    logging.info("closing connections")
    logging.info("exiting main loop")
    logging.info("exit with code 1 - exception")
    exit(1)




