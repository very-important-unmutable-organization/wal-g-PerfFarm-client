import os
import subprocess
import sys
import argparse
from tempfile import TemporaryDirectory
import logging

WALG_REPO_URL = 'https://github.com/wal-g/wal-g'


logging.basicConfig(
    format='[%(levelname)s] [%(asctime)s]  %(message)s',
    level=logging.INFO,
    datefmt='%Y/%m/%d %H:%M:%S',
)


def run_command(command, shell=False):
    if not shell:
        stdout = subprocess.PIPE
        stderr = subprocess.PIPE
    else:
        stdout = sys.stdout
        stderr = sys.stderr

    p = subprocess.Popen(
        [command],
        shell=True,
        stdout=stdout,
        stderr=stderr,
    )

    ret_code = p.wait()
    if ret_code != 0:
        raise RuntimeError("process finished with non-zero code")

    if not shell:
        return p.stdout.read().decode(), p.stderr.read().decode()

    return None, None


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

        run_command('go mod vendor', shell=True)
        run_command('make pg_install', shell=True)

        logging.info('build of walg finished!')


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
