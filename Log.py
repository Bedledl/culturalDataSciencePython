from datetime import datetime


def log(string: str):
    print(f"{datetime.now()}: {string}")