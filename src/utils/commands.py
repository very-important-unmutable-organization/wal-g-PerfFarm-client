import logging
import subprocess
from typing import Tuple, Optional


def run_command(command) -> Tuple[int, str, str]:
    return run_command_(command)


def run_command_out_to_shell(command) -> int:
    code, _, _ = run_command_(command, out_to_shell=True)

    return code


def run_command_(command, out_to_shell=False) -> Tuple[int, Optional[str], Optional[str]]:
    logging.info(f'running {command}')

    completed_process = subprocess.run(
        [command],
        shell=True,
        capture_output=not out_to_shell,
        text=True,
    )

    return completed_process.returncode, completed_process.stdout, completed_process.stderr
