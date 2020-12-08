from datetime import datetime
from models import User
import random
import hashlib
from sqlalchemy import text

def gen_token():
    token = hashlib.md5(bytes(int(random * 10000000.0))).hexdigest()
    return token

def valid(id, token):
    res = User.query.filter(User.id == id).filter(User.token == token).filter(text(f'EXPIRATION<{datetime}'))
    return res is not None