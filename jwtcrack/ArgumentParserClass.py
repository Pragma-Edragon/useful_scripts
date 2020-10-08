import argparse


class MyArgumentParser(argparse.ArgumentParser):

    def __init__(self, *args, **kwargs):
        super(MyArgumentParser, self).__init__(*args, **kwargs)
        self.error_message = ''

    def error(self, message):
        self.error_message = message

    def add_arguments(self):
        super().add_argument(
            '-f',
            action='store',
            required=True,
            help='Filename. No default value'
        )
        super().add_argument(
            '-w',
            '--workers',
            default=1,
            action='store',
            required=False,
            help='Amount of workers. Default is 1'
        )
        super().add_argument(
            '-v',
            type=str,
            metavar='JWT',
            action='store',
            required=True,
            help='Encoded Json Web Token. No default value'
        )

    def parse_args(self, *args, **kwargs):
        # catch SystemExit exception to prevent closing the application
        result = None
        try:
            result = super().parse_args(*args, **kwargs)
        except SystemExit:
            pass
        except TypeError:
            pass
        return result
