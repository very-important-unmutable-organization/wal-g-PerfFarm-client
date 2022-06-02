import argparse
import logging
import os
from tempfile import TemporaryDirectory

from utils.commands import run_command, run_command_out_to_shell

WALG_REPO_URL = 'https://github.com/wal-g/wal-g'

logging.basicConfig(
    format='[%(levelname)s] [%(asctime)s]  %(message)s',
    level=logging.INFO,
    datefmt='%Y/%m/%d %H:%M:%S',
)


def add_metainfo_files(commit):
    run_command(f'git show -s --format=%ct {commit} > /tmp/commit_time')
    with open('/tmp/commit_sha', 'w') as f:
        f.write(commit)


def build_walg(commit):
    with TemporaryDirectory() as tempdir:
        logging.info(f'clonning walg repo from {WALG_REPO_URL}')
        run_command(f'git clone {WALG_REPO_URL} {tempdir}')
        logging.info('walg repo clonned')

        try:
            logging.info(f'checking out commit {commit}')
            os.chdir(tempdir)
            run_command(f'git checkout {commit}')
        except RuntimeError:
            logging.error(f'unknown commit for walg repo: {commit}')
            raise

        logging.info(f'checkout of {commit} succeed')
        logging.info('starting build of walg')

        os.chdir(tempdir)

        run_command_out_to_shell('go mod vendor')
        run_command_out_to_shell('make pg_install')

        logging.info('build of walg finished!')

        add_metainfo_files(commit)
        logging.info('added commit time in /tmp/commit_time')


def parse_args():
    parser = argparse.ArgumentParser(
        prog='build-walg',
        description='program to build wal-g binary from certain commit'
    )
    parser.add_argument('--commit', required=True, type=str, help='commit to build wal-g from')

    return parser.parse_args()


def main():
    args = parse_args()
    build_walg(args.commit)


if __name__ == '__main__':
    main()
