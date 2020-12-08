from datetime import date
from models import User
import random
import hashlib


def gen_token():
    token = hashlib.md5(bytes(int(random * 10000000.0))).hexdigest()
    return token


def valid(tid, token):
    res = User.query.filter(User.id == tid).filter(User.token == token)
    if res is not None:
        print(res)
    #if res is not None:
    #    if date(res.expiration) < date.today():
    #        return True

    return res is not None


