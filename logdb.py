from datetime import datetime, timedelta, date
from models import User, UserSchema, Log
from flask import (make_response, abort, request)
from config import db
from valid import gen_token, valid


def log_access(user_id, stat ):
    lg = Log(id_user = user_id, method = request.method, status = stat, ip = request.remote_addr, url = request.url, time = datetime.now())
    db.session.add(lg)
    db.session.commit()
