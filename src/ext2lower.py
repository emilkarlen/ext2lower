import shutil
import sys
import time
from pathlib import Path
from typing import Optional, Dict, Sequence, Tuple

CMD_EXE = 'x'
CMD_DRY = 'd'


def exit_failure(msg: str):
    print(msg, file=sys.stderr)
    sys.exit(1)


def main():
    if len(sys.argv) < 2:
        exit_failure(usage())
    cmd = sys.argv[1]
    if cmd in ['-h', '--help']:
        print(usage())
        sys.exit(0)

    if len(sys.argv) != 2:
        exit_failure(usage())

    if cmd == CMD_EXE:
        _cli_execute()
    elif cmd == CMD_DRY:
        _cli_dry()
    else:
        exit_failure('Unknown command: ' + cmd)


def _cli_execute():
    exit_failure('execute: todo')


def _cli_dry():
    exit_failure('execute: todo')


def log(msg):
    print(msg, file=sys.stderr)


def usage() -> str:
    return _USAGE.format(
        CMD_EXE=CMD_EXE,
        CMD_DRY=CMD_DRY,
    )


_USAGE = """\
COMMANDS
  {CMD_EXE}   Rename files
  {CMD_DRY}   Run dry - print what had been done by 'x'"""

if __name__ == '__main__':
    main()
