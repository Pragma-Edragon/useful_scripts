import time


class ProgressBar(object):
    start = time.time()

    def output(self):
        getcurtime = round(float(time.time()) - float(ProgressBar.start), 1)
        print(
            f"\r[+] Time elapsed: {getcurtime}s", end=''
        )
