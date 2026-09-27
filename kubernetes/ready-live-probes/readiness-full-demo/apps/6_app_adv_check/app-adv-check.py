import logging
import os
import uuid
import psycopg2
from flask import Flask
from flask import make_response

# Initializations
app = Flask("probes-best-practice")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')

test_account = {
    'name-prefix': 'test-ready-',
    'email': 'ready-test@ready-test.com'
    }

DB_HOST = os.environ.get("DB_HOST", "postgres-postgresql.default.svc.cluster.local")
DB_PORT = os.environ.get("DB_PORT", "5432")

def get_db_conn():
    return psycopg2.connect(user = "postgres", password = "postgres", host = DB_HOST, port = DB_PORT, connect_timeout = 3)

def run_pg_modify(clause, params=None):
    conn = None
    try:
        conn = get_db_conn()
        cur = conn.cursor()
        cur.execute(clause, params)
        conn.commit()
        return True
    except Exception as e:
        logging.error(f"error while performing DB opertaion - {clause}")
        logging.exception(e)
        return None
    finally:
        # Close on the error path too, instead of leaving it to the garbage
        # collector.
        if conn is not None:
            conn.close()


def run_pg_query(query, params=None):
    conn = None
    try:
        conn = get_db_conn()
        cur = conn.cursor()
        cur.execute(query, params)
        return cur.fetchall()
    except Exception as e:
        logging.error(f"error while fetching information from DB using query - {query}")
        logging.exception(e)
        return None
    finally:
        if conn is not None:
            conn.close()

def can_read_from_db():
    return run_pg_query('SELECT * FROM accounts LIMIT 1;')

def can_write_from_db(account_name):
    return run_pg_modify(
        'INSERT INTO accounts(name,owner_email,created_on) VALUES(%s, %s, CURRENT_DATE);',
        (account_name, test_account["email"]),
    )

def can_delete_from_db(account_name):
    return run_pg_modify('DELETE FROM accounts WHERE name = %s', (account_name,))


def do_ready_check_db_operation():

    # Check read from DB. An empty table is a healthy result, so only None
    # means the query itself failed.
    if can_read_from_db() is None:
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
    return make_response("ok", 200)


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
