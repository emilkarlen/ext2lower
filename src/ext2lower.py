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


class Reporter:
    def __init__(self, channel):
        self._channel = channel

    def report(self, src: str, dst: Optional[str]):
        self._channel.write(src + '\n')


def _cli_execute():
    reporter = Reporter(sys.stdout)
    _do_it(reporter)
    _cli_dry()


def _cli_dry():
    reporter = Reporter(sys.stderr)
    _do_it(reporter)


def _do_it(reporter: Reporter):
    for path_str in sys.stdin.readlines():
        src_path = path_str.strip()
        dst_path = rename(src_path)
        reporter.report(str(src_path), dst_path)


def rename(src: str) -> Optional[str]:
    return None


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
