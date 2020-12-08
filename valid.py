from datetime import date, datetime
from models import User
import random
import hashlib


def gen_token():
    token = hashlib.md5(bytes(random.randint(1, 10000000))).hexdigest()
    return token


def valid(tid, token):
    res = User.query.filter(User.id == tid).filter(User.token == token)
    if res is not None:
        print(res)
        dt = datetime.strptime(res.token, "%Y-%m-%d %H:%M:%S")
        if dt >= datetime.now:
            return False


    #if res is not None:
    #    if date(res.expiration) < date.today():
    #        return True

    return res is not None

def valid(token):
    res = User.query.filter(User.token == token).one_or_none()
    print(res)
    if res is not None:
        if res.expiration >= datetime.now():
            return True

    print("Pizdec")
    return False

