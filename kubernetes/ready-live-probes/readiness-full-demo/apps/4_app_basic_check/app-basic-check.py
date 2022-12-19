import os
import logging
import time
import psycopg2
from distutils.util import strtobool
from flask import Flask
from flask import make_response

# Initializations
app = Flask("probes-best-practice")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')


def do_ready_check_db_operation():
    try:
        conn = psycopg2.connect(user = "postgres", password = "postgres", host = "postgres-postgresql.default.svc.cluster.local", port = "5432")
        cur = conn.cursor()
        cur.execute('SELECT * FROM accounts;')
        rows = cur.fetchall()
        conn.close()
    except Exception as e:
        logging.error("error while fetching information from DB")
        logging.exception(e)
        return None
    return rows


@app.route('/live_check')
def live_check():
    return make_response(200)


@app.route('/ready_check')
def ready_check():
    db_ready_reponse = do_ready_check_db_operation()

    if db_ready_reponse:
        logging.info("ready check passed)")
        return make_response("ok", 200)
    else:
        logging.error("Got an exception during DB checks")
        logging.error("Error during ready checks")
        return make_response("ready error", 500)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
