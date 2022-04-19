import os

POSTGRES_BIN = '/usr/lib/postgresql/13/bin'
POSTGRES_CONFIG_NAME = 'postgresql.conf'
POSTGRES_PGDATA = os.environ['PGDATA']
POSTGRES_PASSWORD = ''

MINIO_POSTGRES_BACKUP_BUCKET = 'pgbackup'
MINIO_ACCESS_KEY = 'admin'
MINIO_SECRET_KEY = 'admin_password'
MINIO_ENDPOINT = 'minio:9000'

WALG_CONFIG_PATH = '/opt/.walg.json'
