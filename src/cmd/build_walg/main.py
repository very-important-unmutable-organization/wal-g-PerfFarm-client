import argparse
import json
import logging
import os
from tempfile import TemporaryDirectory

from utils.commands import run_command, run_command_out_to_shell

logging.basicConfig(
    format='[%(levelname)s] [%(asctime)s]  %(message)s',
    level=logging.INFO,
    datefmt='%Y/%m/%d %H:%M:%S',
)


def add_metainfo_files(repo, commit_sha):
    _, commit_time, _ = run_command(f'git show -s --format=%ct {commit_sha}')

    data = {
        'commit_time': commit_time,
        'commit_sha': commit_sha,
        'repo': repo,
    }

    with open('/tmp/build-info.json', 'w') as f:
        json.dump(data, f)

    print(data)


def build_walg(repo, commit):
    with TemporaryDirectory() as tempdir:
        logging.info(f'clonning walg repo from {repo}')
        ret_code, out, err = run_command(f'git clone {repo} {tempdir}')
        if ret_code != 0:
            raise RuntimeError(f"walg repo cannot be cloned. out: {out}; err: {err}")

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

        add_metainfo_files(repo, commit)
        logging.info('added commit time in /tmp/commit_time')


def parse_args():
    parser = argparse.ArgumentParser(
        prog='build-walg',
        description='program to build wal-g binary from certain commit'
    )
    parser.add_argument(
        '--commit',
        required=True,
        type=str,
        help='commit to build wal-g from'
    )
    parser.add_argument(
        '--repo',
        required=False,
        type=str,
        default='https://github.com/wal-g/wal-g',
        help='link to repo with walg (for testing forks). by default points to walg github repository.'
    )

    return parser.parse_args()


def main():
    args = parse_args()
    build_walg(args.repo, args.commit)


if __name__ == '__main__':
    main()
