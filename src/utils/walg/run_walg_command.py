from typing import Tuple

from utils.commands import run_command, run_command_out_to_shell
from utils.const import WALG_CONFIG_PATH


def _walg_generate_command(command: str) -> str:
    return f'wal-g --config {WALG_CONFIG_PATH} {command}'


def run_walg_command(command: str) -> Tuple[int, str, str]:
    return run_command(_walg_generate_command(command))


def time_walg_command(command: str, time_format: str) -> Tuple[int, str, str]:
    return run_command(f'/usr/bin/time -f "{time_format}" {_walg_generate_command(command)}')


def run_walg_command_out_to_shell(command) -> int:
    return run_command_out_to_shell(_walg_generate_command(command))
