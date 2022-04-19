import logging
import os
import shutil

import psycopg2

from utils.commands import run_command, run_command_out_to_shell
from utils.exceptions.postgres import InitdbPgdataNotEmpty, PostgresException
from utils.const import POSTGRES_BIN, POSTGRES_PGDATA, POSTGRES_CONFIG_NAME, WALG_CONFIG_PATH


def initdb():
    logging.info(f'running initdb in {POSTGRES_PGDATA}')
    initdb_path = os.path.join(POSTGRES_BIN, 'initdb')

    ret_code, out, err = run_command(f'{initdb_path} $PGDATA')

    if ret_code == 0:
        logging.info('initdb succeed')
        return

    # initdb has nonzero return code
    initdb_exist_log = f'initdb: error: directory "{POSTGRES_PGDATA}" exists but is not empty'
    if initdb_exist_log in err:
        logging.info(f'{POSTGRES_PGDATA} directory is not empty')
        raise InitdbPgdataNotEmpty()

    logging.error(f'unknown error occurred while initdb process run. stdout: {out}, stderr: {err}')
    raise PostgresException()


def postgres_running():
    logging.info('trying to connect to postgres')
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='postgres',
            user='postgres',
        )
        conn.close()
    except psycopg2.OperationalError:
        logging.info('connection refused')
        return False

    logging.info('connection to postgres succeed!')
    return True


def configure_postgres():
    with open(os.path.join(POSTGRES_PGDATA, POSTGRES_CONFIG_NAME), 'a') as f:
        f.writelines([
            f'archive_mode = on\n',
            f"archive_command = '/usr/bin/timeout 600 /usr/bin/wal-g --config={WALG_CONFIG_PATH} wal-push %p'\n",
            f'archive_timeout = 600\n',
        ])


def start_postgres():
    logging.info('trying to start postgres')
    if postgres_running():
        logging.info('postgres is already running')
        return

    logging.info('postgres is not running now, starting')

    try:
        initdb()
    except InitdbPgdataNotEmpty:
        shutil.rmtree(POSTGRES_PGDATA)
        initdb()

    logging.info('configuring postgres for pushing of wal archives')
    configure_postgres()
    logging.info('configuring succeed!')

    # initdb succeed
    ret_code = run_command_out_to_shell(f'{POSTGRES_BIN}/pg_ctl start')
    # ret_code, out, err = run_command(...)
    # I would like to capture output of this command, but in this case the program is just hangs :(

    if ret_code != 0:
        logging.error(f'Error occurred while running pg_ctl start.')
        raise PostgresException()

    if not postgres_running():
        logging.error('postgres is not running after pg_ctl start')
        raise PostgresException()

    logging.info('postgres is now running!')
    return
