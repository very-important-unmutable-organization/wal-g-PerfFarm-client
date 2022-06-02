import os
from datetime import datetime
from typing import List

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from internal.base.result import Result


class Sender:
    def __init__(self, addr: str):
        self.addr = addr

    def send_batch(self, batch: List[Result], commit_sha: str, commit_time: datetime):
        url = f'{self.addr}/runs'
        uname = os.uname()
        os_str = f'{uname.sysname} {uname.machine} {uname.release}'

        retry_strategy = Retry(
            total=5,
            method_whitelist=["POST"],  # retry on post requests to
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)

        with requests.Session() as session:
            session.mount('http://', adapter)
            session.mount('https://', adapter)

            resp = session.post(
                url,
                timeout=3,
                json={
                    'commit_sha': commit_sha,
                    'commit_time': commit_time.isoformat(),
                    'os': os_str,
                    'client_version': 'хуй соси',
                    'client_environment': 'губой тряси',
                    'metrics': [
                        result.to_dict() for result in batch
                    ]
                },
            )

            if resp.status_code != 200:
                print(resp.text)
                raise RuntimeError("unable to send results to the server, response code is not successful")
