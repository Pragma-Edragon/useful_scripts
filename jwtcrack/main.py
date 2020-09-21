from sys import argv

import jwt
import os
from termcolor import colored

USAGE = colored("argv[0] - program name\n"
                "argv[1] - filename\n"
                "argv[2] - encoded jwt\n", 'red')
os.system('color')


def brute_key(fun):
    def wrapper(*args):
        data = str(next(fun(*args))).splitlines()
        decoded = ""
        for tryes in range(len(data)):
            try:
                decoded += str(jwt.decode(argv[2], data[tryes], algorithms='HS256'))
            except jwt.exceptions.InvalidSignatureError:
                pass
            else:
                if decoded is not None:
                    return colored(f"[+] {decoded}", 'green')
    return wrapper


@brute_key
def yield_file(filename: str) -> object:
    data = ""
    if filename:
        try:
            with open(filename, 'r') as file:
                data += file.read()
                file.close()
        except Exception as error:
            print(error)
    yield data


if __name__ == '__main__':
    if len(argv) < 3:
        print(USAGE)
        quit()
    if yield_file(argv[1]):
        print(yield_file(argv[1]))
    else:
        print(colored("[-] Nothing found. Try another list", 'yellow'))
