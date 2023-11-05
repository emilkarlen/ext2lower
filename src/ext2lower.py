import shutil
import sys
import time
from pathlib import Path
from typing import Optional, Dict, Sequence, Tuple, Callable

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

    def report(self, src: Path, dst: Optional[Path]):
        if dst is None:
            self._channel.write(str(src) + '\n')
        else:
            self._channel.write('{} -> {}\n'.format(src, dst))


def _cli_execute():
    def renamer(src: Path, dst: Path):
        if dst.exists():
            exit_failure('Target exists: {} -> {}'.format(src, dst))

        try:
            src.rename(dst)
        except OSError as ex:
            print('Failed to rename: {} -> {}'.format(src, dst), file=sys.stderr)
            exit_failure(str(ex))

    reporter = Reporter(sys.stdout)
    _do_it(reporter, renamer)
    _cli_dry()


def _cli_dry():
    def renamer(src: Path, dst: Path):
        pass

    reporter = Reporter(sys.stderr)
    _do_it(reporter, renamer)


def _do_it(reporter: Reporter, renamer: Callable[[Path, Path], None]):
    for path_str in sys.stdin.readlines():
        src_path = Path(path_str.strip())
        if not src_path.exists():
            exit_failure('File does not exist: {}'.format(src_path))
        dst_path = new_name(src_path)
        if dst_path is not None:
            renamer(src_path, dst_path)
        reporter.report(src_path, dst_path)


def new_name(src: Path) -> Optional[Path]:
    suffix = src.suffix
    suffix_lower = suffix.lower()
    if suffix != suffix_lower:
        return src.with_suffix(suffix_lower)
    else:
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
