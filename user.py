from datetime import datetime, timedelta, date
from models import User, UserSchema
from flask import (make_response, abort)
from config import db
from valid import gen_token, valid
from logdb import log_access

def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

def acq_token(user_id):
    us = (
        User.query.filter(User.id == user_id)
            .one_or_none()
    )

    if us is not None:

        us.token = gen_token()
        us.expiration = (datetime.strptime(str(us.expiration), "%Y-%m-%d %H:%M:%S") + timedelta(days = 30))
        db.session.commit
        log_access(user_id, 200)
        u = UserSchema().dump(us)
        return u
    else:
        log_access(user_id, 404)
        abort(
            404, f'Failed to locate a users id {user_id}'
        )
def read_all(token):
    if not valid(token):
        log_access(token, 403)
        abort(403, 'Phony token detected')

    sc = User.query.order_by(User.id).all()
    s = UserSchema(many = True)
    if sc is not None:
        log_access(token, 200)
        return s.dump(sc)
    else:
        log_access(token, 404)
        abort(404, "Not found")


def read_one(token, user_id):

    uz = (User.query.filter(User.id == user_id).one_or_none())
    if uz is not None:
        if uz.token != token:
            log_access(user_id, 401)
            abort(401, 'Phony token detected')
        schema = UserSchema()
        log_access(user_id, 200)
        return schema.dump(uz)
    else:
        log_access("NONE", 400)
        abort(400, f"User not found for Id: {user_id}")


def create(user):

    name = user.get('name')
    lg = user.get('lg')
    ps = user.get('timestamp')

    existing = User.query \
        .filter(User.name == name) \
        .filter(User.password == ps) \
        .filter(User.login == lg) \
        .one_or_none()

    if existing is None:
        new = User(name = name, password = ps, login = lg, token = gen_token(), \
                          expiration = (datetime.now() + timedelta(days = 30)))
        schema = UserSchema()
        db.session.add(new)
        db.session.commit()

        log_access(new.id, None, 404)
        return schema.dump(new)

    else:
        log_access("NONE", 404)
        abort(404, f'User {name} {lg} exists already')


def update(user, user_id, token):
    us = (
        User.query.filter(User.id == user_id)
            .one_or_none()
    )

    if us is not None:
        if us.token != token:
            log_access(user_id, None, 403)
            abort(403, "Tokens didn't match")


        us.name = user.get('name')
        us.login = user.get('login')
        us.id = user.get('id')
        sc = UserSchema()
        db.session.commit
        log_access(user_id, None, 200)
        return sc.dump(us)
    else:
        log_access(None, 200)
        abort(
            404, 'Failed to locate a users id {user_id}'
        )


def delete(user_id, token):
    us = (
        User.query.filter(User.id == user_id)
            .one_or_none()
    )

    if us is not None:
        if us.token != token:
            log_access(user_id, None, 403)
            abort(403, "Tokens didn't match")

        db.session.delete(us)
        db.session.commit
    else:
        log_access(None, 200)
        abort(
            404, 'Failed to locate a users id {user_id}'
        )