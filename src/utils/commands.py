import logging
import subprocess
from typing import Tuple, Optional


def run_command(command) -> Tuple[int, str, str]:
    return _run_command(command)


def run_command_out_to_shell(command) -> int:
    code, _, _ = _run_command(command, out_to_shell=True)

    return code


def _run_command(command, out_to_shell=False) -> Tuple[int, Optional[str], Optional[str]]:
    logging.debug(f'running {command}')

    completed_process = subprocess.run(
        [command],
        shell=True,
        capture_output=not out_to_shell,
        text=True,
    )

    return completed_process.returncode, completed_process.stdout, completed_process.stderr
