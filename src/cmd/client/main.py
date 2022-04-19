import logging
import time

from internal.wrappers.random_wal_generator import RandomWalGenerator
from utils.generate_walg_config import generate_walg_config
from utils.postgres.start import start_postgres

logging.basicConfig(
    format='[%(levelname)s] [%(asctime)s]  %(message)s',
    level=logging.INFO,
    datefmt='%Y/%m/%d %H:%M:%S',
)


def main():
    generate_walg_config()
    start_postgres()
    generator = RandomWalGenerator()
    generator.prepare(None)


if __name__ == '__main__':
    main()
    time.sleep(999999)
