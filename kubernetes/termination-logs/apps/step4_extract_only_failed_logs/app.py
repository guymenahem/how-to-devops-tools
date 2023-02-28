import logging
import traceback


# Initializations
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')

def write_exception_to_file(e, filename='/dev/termination-log'):
    with open(filename, 'w') as f:
        # write exception message to file
        f.write(str(e) + '\n')
        # write stack trace to file
        traceback.print_exc(file=f)

try:
    logging.info("start service")
    raise Exception("unauthorized operation")
except Exception as e:
    logging.exception(e)
    write_exception_to_file(e) 
    logging.info("closing connections")
    logging.info("exiting main loop")
    logging.info("exit with code 1 - exception")
    exit(1)


