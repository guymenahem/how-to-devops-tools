import os
import logging
import time
import uuid
import psycopg2
from distutils.util import strtobool
from flask import Flask
from flask import make_response

# Initializations
app = Flask("probes-best-practice")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')

test_account = {
    'name-prefix': 'test-ready-',
    'email': 'ready-test@ready-test.com'
    }

def get_db_conn():
    return psycopg2.connect(user = "postgres", password = "postgres", host = "postgres-postgresql.default.svc.cluster.local", port = "5432")

def run_pg_modify(clause):
    try:
        conn = get_db_conn()
        cur = conn.cursor()
        cur.execute(clause)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        logging.error(f"error while performing DB opertaion - {clause}")
        logging.exception(e)
        return None
    

def run_pg_query(query):
    try:
        conn = get_db_conn()
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()
    except Exception as e:
        logging.error(f"error while fetching information from DB using query - {query}")
        logging.exception(e)
        return None
    return rows

def can_read_from_db():
    return run_pg_query(f'SELECT * FROM accounts LIMIT 1;')

def can_write_from_db(account_name):
    return run_pg_modify(f'INSERT INTO accounts(name,owner_email,created_on) VALUES(\'{account_name}\', \'{test_account["email"]}\', CURRENT_DATE);')

def can_delete_from_db(account_name):
    return run_pg_modify(f'DELETE FROM accounts WHERE name =\'{account_name}\'')


def do_ready_check_db_operation():

    # Check read from DB
    if not can_read_from_db():
        logging.warning("could not read from DB during ready check")
        return False
    
    # Generate UUID for this check
    run_uuid = test_account['name-prefix'] + str(uuid.uuid1())
    logging.info("selected account name for this run: " + run_uuid)

    # Check write & delete operations
    if not can_write_from_db(run_uuid):
        logging.warning("could not write to DB during ready check")
        return False
    logging.info(f"successfully performed write operations for readiness check of account - {run_uuid}")

    if not can_delete_from_db(run_uuid):
        logging.warning("could not delete from DB during ready check")
        return False
    logging.info(f"successfully performed delete operations for readiness check of account - {run_uuid}")

    return True

@app.route('/live_check')
def live_check():
    return make_response(200)


@app.route('/ready_check')
def ready_check():
    db_ready_reponse = do_ready_check_db_operation()

    if db_ready_reponse:
        logging.info("ready check passed")
        return make_response("ok", 200)
    else:
        logging.error("Error during ready checks")
        return make_response("ready error", 500)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
