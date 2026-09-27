import logging
import os
import psycopg2
from flask import Flask
from flask import make_response

# Initializations
app = Flask("probes-best-practice")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')

DB_HOST = os.environ.get("DB_HOST", "postgres-postgresql.default.svc.cluster.local")
DB_PORT = os.environ.get("DB_PORT", "5432")


def do_ready_check_db_operation():
    conn = None
    try:
        conn = psycopg2.connect(user = "postgres", password = "postgres", host = DB_HOST, port = DB_PORT, connect_timeout = 3)
        cur = conn.cursor()
        cur.execute('SELECT * FROM accounts;')
        return cur.fetchall()
    except Exception as e:
        logging.error("error while fetching information from DB")
        logging.exception(e)
        return None
    finally:
        # Close on the error path too, instead of leaving it to the garbage
        # collector.
        if conn is not None:
            conn.close()


@app.route('/live_check')
def live_check():
    return make_response("ok", 200)


@app.route('/ready_check')
def ready_check():
    db_ready_reponse = do_ready_check_db_operation()

    # An empty table is a healthy result, so only None means the query failed.
    if db_ready_reponse is not None:
        logging.info("ready check passed")
        return make_response("ok", 200)
    else:
        logging.error("Got an exception during DB checks")
        logging.error("Error during ready checks")
        return make_response("ready error", 500)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
