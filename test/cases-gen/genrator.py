import sys
from pathlib import Path
from typing import Optional, Dict, Sequence, Tuple


CASES_FILE = 'cases.txt'
TEMPLATE_DIR = 'template'

SUB_DIR_SYMBOL = 'SUB_DIR'


def exit_failure(msg: str):
    print(msg, file=sys.stderr)
    sys.exit(1)


class FileName:
    def __init__(self, original: str, renamed: Optional[str]):
        self.original = original
        self.renamed = renamed


class OriginalFileNamesFormatter:
    def __init__(self, file_names: Sequence[FileName]):
        self._file_names = file_names

    def __format__(self, format_spec):
        return '\n'.join(
            [fn.original for fn in self._file_names]
        )


class SymRefFormatter:
    def __init__(self, symbol: str):
        self._symbol = symbol

    def __format__(self, format_spec):
        return '@[{}]@'.format(self._symbol)


class FileNameRenamingsFormatter:
    def __init__(self, file_names: Sequence[FileName]):
        self._file_names = file_names

    @staticmethod
    def _format_file_name(file_name: FileName):
        if file_name.renamed is None:
            return file_name.original
        else:
            return '{} -> {}'.format(file_name.original, file_name.renamed)

    def __format__(self, format_spec):
        return '\n'.join(
            [self._format_file_name(fn) for fn in self._file_names]
        )


class FilesFormatter:
    def __init__(self, file_names: Sequence[FileName]):
        self._file_names = file_names

    @staticmethod
    def _format_file_name(file_name: FileName):
        return '  file {}'.format(file_name.original)

    def __format__(self, format_spec):
        return '\n'.join(
            [self._format_file_name(fn) for fn in self._file_names]
        )


def is_empty_file_matcher(file_name: str) -> str:
    return '  {} : type file && contents is-empty'.format(file_name)


class OriginalFilesFormatter:
    def __init__(self, file_names: Sequence[FileName]):
        self._file_names = file_names

    def __format__(self, format_spec):
        return '\n'.join(
            [is_empty_file_matcher(fn.original) for fn in self._file_names]
        )


class RenamedFilesFormatter:
    def __init__(self, file_names: Sequence[FileName]):
        self._file_names = file_names

    def _dst_file(self, fn: FileName) -> str:
        return fn.original if fn.renamed is None else fn.renamed

    def __format__(self, format_spec):
        return '\n'.join(
            [is_empty_file_matcher(self._dst_file(fn)) for fn in self._file_names]
        )


def in_subdir(subdir: str, fn: FileName) -> FileName:
    def sub(d: str, f: str) -> str:
        return str(Path(d) / f)

    original = sub(subdir, fn.original)
    renamed = None if fn.renamed is None else sub(subdir, fn.renamed)

    return FileName(original, renamed)


def definitions(file_names: Sequence[FileName]) -> str:
    subdir_ref = format(SymRefFormatter(SUB_DIR_SYMBOL))
    subdir_files = [in_subdir(subdir_ref, fn) for fn in file_names]

    return DEFINITIONS.format(
        SUB_DIR_SYMBOL=SUB_DIR_SYMBOL,
        ORIGINAL_FILE_LIST=OriginalFileNamesFormatter(file_names),
        RENAMINGS_FILE_LIST=FileNameRenamingsFormatter(file_names),
        FILES=FilesFormatter(file_names),
        ORIGINAL_FILES_MATCHERS=OriginalFilesFormatter(file_names),
        RENAMED_FILES_MATCHERS=RenamedFilesFormatter(file_names),
        ORIGINAL_FILE_LIST__SUBDIR=OriginalFileNamesFormatter(subdir_files),
        RENAMINGS_FILE_LIST__SUBDIR=FileNameRenamingsFormatter(subdir_files),
    )


def read_cases(path: Path) -> Dict[str, FileName]:
    def parse_line(s: str) -> Tuple[str, FileName]:
        parts = s.split()
        if len(parts) == 2:
            return parts[0], FileName(parts[1], None)
        else:
            return parts[0], FileName(parts[1], parts[2])

    ret_val = dict()
    for line in path.read_text().splitlines(keepends=False):
        case_name, file_name = parse_line(line)
        ret_val[case_name] = file_name
    return ret_val


def main():
    if len(sys.argv) != 2:
        exit_failure('Usage CASES-FILE')
    cases_file = Path(sys.argv[1])
    if not cases_file.is_file():
        exit_failure('Not a regular file: ' + str(cases_file))
    cases = read_cases(cases_file)
    print(definitions(list(cases.values())))


DEFINITIONS = """\
def string {SUB_DIR_SYMBOL} = subdir.SUBEXT

def string ORIGINAL_FILE_LIST =
<<EOF
{ORIGINAL_FILE_LIST}
EOF

def string RENAMINGS_FILE_LIST =
<<EOF
{RENAMINGS_FILE_LIST}
EOF

def string ORIGINAL_FILE_LIST_subdir =
<<EOF
{ORIGINAL_FILE_LIST__SUBDIR}
EOF

def string RENAMINGS_FILE_LIST_subdir =
<<EOF
{RENAMINGS_FILE_LIST__SUBDIR}
EOF

def files-source FILES =
{{
{FILES}
}}

def files-matcher MATCHES_ORIGINAL_FILES = matches -full
{{
{ORIGINAL_FILES_MATCHERS}
}}

def files-matcher MATCHES_RENAMED_FILES = matches -full
{{
{RENAMED_FILES_MATCHERS}
}}
"""

if __name__ == '__main__':
    main()
