import logging
import time

from internal.wrappers.random_wal_generator import RandomWalGenerator
from utils.postgres.start import start_postgres

logging.basicConfig(
    format='[%(levelname)s] [%(asctime)s]  %(message)s',
    level=logging.INFO,
    datefmt='%Y/%m/%d %H:%M:%S',
)


def main():
    # TODO walg config generation
    # TODO postgres configuration for wal pushing
    generator = RandomWalGenerator()
    generator.prepare(None)


if __name__ == '__main__':
    main()
    time.sleep(999999)
