import sys
from os.path import isfile
from subprocess import check_output
from typing import Dict, List


RED: str = '\033[1;31m'
YELLOW: str = '\033[1;33m'
NC: str = '\033[0m'  # No Color
CROSS = '❌'
CHECK = '✅'
HELP: str = '\nrun `python3 sanitizer_checker.py -h` for details'


def is_elf_file(file_path: str) -> bool:
    with open(file_path, 'rb') as f:
        header: bytes = f.read(4)
        if header != b'\x7fELF':
            return False
        return True


def detect_sanitizers(file: str) -> Dict:
    """
    Поиск санитайзеров, использованных при сборке
    """
    output: str = check_output(['nm', file]).decode('utf-8')
    # Заполним словарь значениями по умолчанию
    sanitizers: Dict = {
        'AddressSanitizer': {'alias': '_asan', 'is_used': False},
        'MemorySanitizer': {'alias': '_msan', 'is_used': False},
        'ThreadSanitizer': {'alias': '_tsan', 'is_used': False},
        'UndefinedBehaviorSanitizer': {'alias': '_ubsan', 'is_used': False},
        'DataFlowSanitizer': {'alias': '_dfsan', 'is_used': False},
        'LeakSanitizer': {'alias': '_lsan', 'is_used': False},
                        }
    for san in sanitizers:
        if sanitizers[san]['alias'] in output:
            sanitizers[san]['is_used'] = 'True'
    return sanitizers


def print_default_sanitizers(sanitizers: Dict, file: str):
    """
    Печать только одного из трёх санитайзеров (по умолчанию)
    """
    major_sans: List = ['AddressSanitizer', 'MemorySanitizer',
                        'ThreadSanitizer']
    is_used: bool = False
    for san in major_sans:
        if sanitizers[san]['is_used']:
            is_used = True
    if is_used is True:
        print(f'The file {file} was built with a sanitizer:')
    else:
        print(f'The file {file} was not built with any sanitizers:')
    for san in major_sans:
        sign: str = CROSS if sanitizers[san]['is_used'] is False else CHECK
        print(f'{san}: {sign}')


def print_all_sanitizers(sanitizers: Dict, file: str):
    """
    Печать всех санитайзеров, при использовании -a или --all
    """
    is_used: bool = False
    for san in sanitizers:
        if sanitizers[san]['is_used'] is True:
            is_used = True
    if is_used is True:
        print(f'The file {file} was built with the sanitizers:')
    else:
        print(f'The file {file} was not built with any sanitizers:')
    for san in sanitizers:
        sign: str = CROSS if sanitizers[san]['is_used'] is False else CHECK
        print(f'{san}: {sign}')


def print_help_info():
    print(f"""{YELLOW}Usage:{NC} python3 sanitizer_checker.py [file_path] \
[options]

Description:
        List of sanitizers used during file compilation (by default only \
AddressSanitizer, MemorySanitizer, ThreadSanitizer).

Example:
        python3 sanitizer_checker.py test.so

Options:
        -a, --all:  print all detected sanitizers
        -h, --help: print help information""")


def is_valid(args: List) -> bool:
    """
    Проверка аргументов на валидность
    """
    file: str = args[1]
    if isfile(file) is False:
        print(f'{RED}Error:{NC} {file}: file does not exist')
        return False
    if is_elf_file(file) is False:
        print(f'{RED}Error:{NC} {file}: file is not ELF')
        return False
    if len(args) == 3 and args[2] != '-a' and args[2] != '--all':
        print(f'{RED}Error:{NC} {args[2]}: unsupported option{HELP}')
        return False
    return True


def check_sanitizers(args: List):
    """
    Вывод списка использованных санитайзеров
    """
    file: str = args[1]
    sanitizers: Dict = detect_sanitizers(file)
    if len(args) == 2:
        print_default_sanitizers(sanitizers, file)
    else:
        print_all_sanitizers(sanitizers, file)


if __name__ == '__main__':
    args_count: int = len(sys.argv)
    if args_count < 2 or args_count > 3:
        print(f'{YELLOW}Usage:{NC} python3 sanitizer_checker.py [file_path] \
[options]{HELP}')
    else:
        option_pos: int = args_count - 1
        if (sys.argv[option_pos] == '--help' or sys.argv[option_pos] == '-h'):
            print_help_info()
        elif is_valid(sys.argv) is True:
            check_sanitizers(sys.argv)
