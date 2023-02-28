import logging

# Initializations
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')

try:
    s = 1
    raise Exception("unauthorized operation")
except Exception as e:
    logging.exception(e)
    exit(1)


