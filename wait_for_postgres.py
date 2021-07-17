import logging
import os
from time import sleep, time
import dotenv

import psycopg2


def pg_isready(host, user, password, dbname, port):
    while time() - start_time < check_timeout:
        try:
            conn = psycopg2.connect(**vars())
            logger.info("Postgres is ready! ✨ 💅")
            conn.close()
            return True
        except psycopg2.OperationalError as e:
            logger.error(e)
            logger.info(f"Postgres isn't ready. Waiting for {check_interval} {interval_unit}...")
            sleep(check_interval)

    logger.error(f"We could not connect to Postgres within {check_timeout} seconds.")
    return False

if __name__ == "__main__":
    dotenv.read_dotenv()
    global check_timeout, check_interval
    check_timeout = int(os.environ.get("POSTGRES_CHECK_TIMEOUT"))
    check_interval = int(os.environ.get("POSTGRES_CHECK_INTERVAL"))
    interval_unit = "second" if check_interval == 1 else "seconds"
    config = {
        "dbname": os.environ.get("POSTGRES_DB"),
        "user": os.environ.get("POSTGRES_USER"),
        "password": os.environ.get("POSTGRES_PASSWORD"),
        "host": os.environ.get("DATABASE_URL"),
        "port": os.environ.get("POSTGRES_PORT")
    }

    start_time = time()
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
    pg_isready(**config)