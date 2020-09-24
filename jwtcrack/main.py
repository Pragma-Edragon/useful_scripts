from sys import argv

import jwt
import os
import time
import chardet
from termcolor import colored

USAGE = colored("argv[0] - program name\n"
                "argv[1] - filename\n"
                "argv[2] - encoded jwt\n", 'red')
os.system('color')


def progress(iteration: int, max_iter: int, **kwargs):
    # dont want to parse in 1 line, it wont be nice.
    res = time.time() - kwargs['start']
    print(f"\r[+] Progress: {iteration}/{max_iter + 1} :: seconds: {round(res, 1)} "
          f"/ percents: {round(iteration/max_iter * 100, 2)}%", end='')


def file_encoding(filename: str):
    with open(filename, 'rb') as file:
        data = file.read(60000)
        res = chardet.detect(data)
        file.close()
    if res['confidence'] >= 0.5:
        return str(res['encoding'])
    else:
        return None


def brute_key(fun):
    def wrapper(*args):
        decoded = ""
        data = str(next(fun(*args))).splitlines()
        start = time.time()
        for tryes in range(len(data)):
            progress(tryes, len(data), start=start)
            try:
                decoded += str(jwt.decode(argv[2], data[tryes], algorithms='HS256'))
            except jwt.exceptions.InvalidSignatureError:
                pass
            else:
                if decoded is not None:
                    return colored(f"\n[+] {decoded}", 'green')

    return wrapper


@brute_key
def yield_file(filename: str) -> object:
    data = ""
    encoding = file_encoding(filename)
    print(encoding)
    if encoding is not None:
        if filename:
            print(colored(f'[+] File encoding: {encoding}', 'green'))
            try:
                with open(filename, encoding=encoding, mode='r') as file:
                    data += file.read()
                    file.close()
            except Exception as error:
                raise
        yield data
    else:
        print(colored("[-]Can't detect file encoding.", 'red'))
        quit()


if __name__ == '__main__':
    if len(argv) < 3:
        print(USAGE)
        quit()
    try:
        decoded = yield_file(argv[1])
        if decoded:
            print(decoded)
        else:
            print(colored("[-] Nothing found. Try another list", 'yellow'))
    except KeyboardInterrupt:
        print(colored("\n[-] Keyboard Interrupt", 'red'))
