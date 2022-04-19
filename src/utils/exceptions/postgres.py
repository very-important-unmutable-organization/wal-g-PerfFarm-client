from utils.exceptions.base import WalgPerformanceFarmBase


class PostgresException(WalgPerformanceFarmBase):
    pass


class InitdbPgdataNotEmpty(PostgresException):
    def __str__(self):
        return 'initdb command is not succeeded because $PGDATA directory is not empty'
