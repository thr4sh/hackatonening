from datetime import datetime, timedelta, date
from models import User, UserSchema, Log
from flask import (make_response, abort, request)
from config import db
from valid import gen_token, valid

#hacky af, i like it. image running this with 10^10 entries
def log_access(user_id, token, stat ):
    lid = str(int(Log.query.order_by(Log.id).all()[-1].id) + 1)

    lg = Log(id = lid, id_user = user_id, method = request.method, status = stat, ip = request.remote_addr, url = request.url, time = datetime.now())
    db.session.add(lg)
    db.session.commit()

def log_access(token, stat ):
    lid = str(int(Log.query.order_by(Log.id).all()[-1].id) + 1)
    res = User.query.filter(User.token == token).one_or_none()
    lg = Log(id = lid, id_user = res.id, method = request.method, status = stat, ip = request.remote_addr, url = request.url, time = datetime.now())
    db.session.add(lg)
    db.session.commit()
