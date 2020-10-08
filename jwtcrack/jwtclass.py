import os
import jwt
import sys
import logging
import chardet
import argparse
import multiprocessing
from termcolor import colored
from ArgumentParserClass import MyArgumentParser


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
        """
        Simple class constructor
        :param token: JSON web token.
        :param filename: parsed filename. No default value
        :param workers: Amount of processes. Default: 1.
        :param encode: File encoding.
        """
        self.token = token
        self.filename = filename
        self.workers = workers
        self.encode = encode

    def file_encoding(self):
        """
        Opening file for read bytes.
        Bytes -> chardet to detect encoding.
        If confidence >= 0.55:
        :return result
        else:
        TODO
        """
        with open(self.filename, 'rb') as file:
            data = file.read(JWTcrack.CHUNK)
            res = chardet.detect(data)
            file.close()
        if float(res['confidence']) >= 0.55:
            self.encode = str(res['encoding'])

    def open_file(self):
        """
        Method for file opening.
        If file in current directory:
        need to check its encoding.
        TODO Else:
        TODO through exception
        :return:
        """
        if self.filename in os.listdir():
            self.file_encoding()
        if self.encode is not None:
            with open(self.filename, 'r', encoding=self.encode) as decoded_data:
                data = decoded_data.read()
                decoded_data.close()
            for keys in data.splitlines():
                yield keys

    def brute_jwt(self, key):
        """
        Inserting random keys from filename,
        splited by newline.
        Trying to decode JWT token.
        TODO return decoded data
        :param key:
        :return:
        """
        try:
            decoded_data = jwt.decode(self.token, key=key, algorithms=['HS256'])
        except jwt.exceptions.InvalidSignatureError:
            pass
        else:
            print(decoded_data)

    def start_cracking(self):
        """
        Main method.
        TODO catch exceptions
        :return:
        """
        data = self.open_file()
        try:
            while (True):
                temp = str(next(data))
                self.brute_jwt(temp)
        except Exception as err:
            pass


author = Author()
print(author.__repr__())
# testing -------
my_parser = MyArgumentParser()
my_parser.add_arguments()
args = my_parser.parse_args()
# check for an error
if my_parser.error_message:
    print(my_parser.error_message)
print(args)
tk = JWTcrack(filename=args.f, token=args.v)
tk.start_cracking()
