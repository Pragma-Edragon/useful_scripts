import os
import jwt
import sys
import logging
import chardet
import multiprocessing
from termcolor import colored
from ArgumentParserClass import MyArgumentParser
from ProgressBarClass import ProgressBar


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
        """
        with open(self.filename, 'rb') as file:
            data = file.read(JWTcrack.CHUNK)
            res = chardet.detect(data)
            file.close()
        if float(res['confidence']) >= 0.55:
            self.encode = str(res['encoding'])
            print(colored(f'\r[+] Found file encoding: {self.encode}', 'green'))
        else:
            logging.critical(colored("\r[-] Can't spot file encoding", 'red'))
            quit()

    def open_file(self):
        """
        Method for file opening.
        If file in current directory:
        need to check its encoding.
        TODO through exception
        :return:
        """
        if self.filename in os.listdir():
            self.file_encoding()
        else:
            logging.error(colored(f"\r[-] No file found: {self.filename}", 'red'))
            quit()
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
        :param key:
        :return: decoded_data
        """
        try:
            decoded_data = jwt.decode(self.token, key=key, algorithms=['HS256'])
        except jwt.exceptions.InvalidSignatureError:
            pass
        else:
            return decoded_data

    def start_cracking(self):
        """
        Main method.
        :return:
        """
        data = self.open_file()
        bar = ProgressBar()
        try:
            while True:
                bar.output()
                temp = str(next(data))
                decoded = self.brute_jwt(temp)
                if decoded:
                    return colored(f"\n[+] {str(decoded)} with key: {temp}", 'green')
        except Exception:
            logging.warning(colored('\r[-] Nothing found. Try another dictionary', 'yellow'))


author = Author()
print(author.__repr__())

my_parser = MyArgumentParser()
my_parser.add_arguments()
args = my_parser.parse_args()

if my_parser.error_message:
    my_parser.print_help()
    quit()

tk = JWTcrack(filename=args.f, token=args.v)
decode = tk.start_cracking()
if decode is not None:
    print(str(decode))

