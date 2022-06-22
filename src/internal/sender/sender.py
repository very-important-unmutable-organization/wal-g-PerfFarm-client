import logging
import os
from datetime import datetime
from typing import List

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from internal.base.result import Result


class Sender:
    def __init__(self, addr: str, login: str, password: str):
        self.addr = addr
        self.login = login
        self.password = password

    def _login(self, session: requests.Session):
        logging.info(f'trying to login to server at {self.addr}')

        url = f'{self.addr}/api/auth/login'
        data = {
            'username': self.login,
            'password': self.password,
        }

        resp = session.post(url, json=data)
        if resp.status_code != 200:
            raise RuntimeError(
                f"unable to login to server. expected status code 200, but was {resp.status_code}. body: {resp.text}"
            )

        access_token = resp.json()['access_token']
        session.headers.update({
            'Authorization': f'Bearer {access_token}'
        })

        logging.info('login succeed')

    @staticmethod
    def _prepare_session(session: requests.Session):
        retry_strategy = Retry(
            total=5,
            method_whitelist=["POST"],  # retry on post requests
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

    def send_batch(self, batch: List[Result], repo: str, commit_sha: str, commit_time: datetime):
        logging.info(f'trying to send batch to server {self.addr}')

        url = f'{self.addr}/api/runs'
        uname = os.uname()
        os_str = f'{uname.sysname} {uname.machine} {uname.release}'

        with requests.Session() as session:
            self._prepare_session(session)
            self._login(session)

            logging.debug(f'repo: {repo}')
            resp = session.post(
                url,
                timeout=3,
                json={
                    'commit_sha': commit_sha,
                    'commit_time': commit_time.isoformat(),
                    'repo': repo,
                    'os': os_str,
                    'client_version': 'хуй соси',
                    'client_environment': 'губой тряси',
                    'metrics': [
                        result.to_dict() for result in batch
                    ]
                },
            )

            if resp.status_code != 200:
                raise RuntimeError(
                    f"unable to send results to the server, response code is not successful. "
                    f"expected 200, but was {resp.status_code}. body: {resp.text}"
                )

        logging.info('all results were sent!')
