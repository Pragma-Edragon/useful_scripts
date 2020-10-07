import os
import jwt
import logging
import chardet
import argparse
import multiprocessing
from termcolor import colored


class Author(object):
    os.system('color')
    __progname__ = 'JWTcrack'
    __author__ = "r1v3n"
    __git__ = "Pragma-Edragon"

    @classmethod
    def __repr__(cls):
        return colored("{line}\n\tAuthor: {aut} \n\tGithub: {git} \n\tProgram Name: {name}\n{line}".format(
            line='-' * 30, aut=cls.__author__, git=cls.__git__, name=cls.__progname__), 'cyan')


class JWTcrack(object):
    CHUNK = 32768

    def __init__(self, token, filename,
                 workers=1, encode=None):
        self.token = token
        self.filename = filename
        self.workers = workers
        self.encode = encode

    def get_arguments(self):
        parser = argparse.ArgumentParser(
            usage="JWTcrack.py [-f] [--workers] [-JWT"
        )
        parser.add_argument('-f',
                            action='store',
                            help='Filename. No default value'
                            )
        parser.add_argument('--workers',
                            default=1,
                            action='store',
                            help='Amount of workers. Default is 1'
                            )
        parser.add_argument('JWT',
                            type=str,
                            metavar='JWT',
                            action='store',
                            help='Encoded Json Web Token. No default value')

        args = parser.parse_args(['-f', '123', '13212'])
        self.filename, self.workers, self.token = vars(args).values()

    def file_encoding(self):
        with open(self.filename, 'rb') as file:
            data = file.read(JWTcrack.CHUNK)
            res = chardet.detect(data)
            file.close()
        if float(res['confidence']) >= 0.55:
            self.encode = str(res['encoding'])

    def open_file(self):
        if self.filename in os.listdir():
            self.file_encoding()
        if self.encode is not None:
            with open(self.filename, 'r', encoding=self.encode) as decoded_data:
                data = decoded_data.read()
                decoded_data.close()
            for keys in data.splitlines():
                yield keys

    def brute_jwt(self, key):
        try:
            decoded_data = jwt.decode(self.token, key=key, algorithms=['HS256'])
        except jwt.exceptions.InvalidSignatureError:
            pass
        else:
            print(decoded_data)

    def start_cracking(self):
        data = self.open_file()
        try:
            while (True):
                temp = str(next(data))
                self.brute_jwt(temp)
        except Exception as err:
            pass


class ProgressBar(object):
    def change_progress(self, iter, max_len):
        print()


author = Author()
print(author.__repr__())
a = JWTcrack(
    'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkYXRhIjoiYWRtaW4xMjMiLCJsb2dpbiI6ImFkbWluIn0._uBdbB9V7c8bXNbmdp5ffy2BN1ElDZfne6DP26ACbeA',
    'test.txt')
a.start_cracking()
