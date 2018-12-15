import multiprocessing
from multiprocessing import freeze_support

import requests


def req(x):
    result = requests.get("http://127.0.0.1:1234/denial_of_service")
    print(result.text[:10])


if __name__=="__main__":
    freeze_support()
    with multiprocessing.Pool(processes=10) as pool:
        pool.map(req, [_ for _ in range(100000)])
