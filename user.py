from datetime import datetime, timedelta
from models import User, UserSchema
from flask import (make_response, abort)
from config import db
from valid import gen_token, valid


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


def read_all(token):
    if not valid(token):
        abort(403, 'Phony token detected')

    sc = User.query.order_by(User.id).all()
    sc = UserSchema(sc, many=True)
    if sc is None:
        return 200, sc
    else:
        abort(404, "Not found")


def read_one(token, user_id):

    uz = (User.query.filter(User.id == user_id).one_or_none())
    if uz is not None:
        if uz.token != token:
            abort(401, 'Phony token detected')
        schema = UserSchema(uz)
        return schema
    else:
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
                          expiration = (datetime.now() + timedelta(days = 30)).strftime(("%Y-%m-%d %H:%M:%S")))
        schema = UserSchema(new)
        db.session.add(new)
        db.session.commit()

        return 201, schema

    else:
        abort(404, f'User {name} {lg} exists already')


def update(user, user_id, token):
    us = (
        User.query.filter(User.id == user_id)
            .one_or_none()
    )

    if us is not None:
        if us.token != token:
            abort(403, "Tokens didn't match")

        qus = User()
        qus.name = user.get('name')
        qus.login = user.get('login')
        qus.id = user.get('id')
        sc = UserSchema(qus)
        db.session.commit
        return 201, sc
    else:
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
            abort(403, "Tokens didn't match")

        db.session.delete(us)
        db.session.commit
    else:
        abort(
            404, 'Failed to locate a users id {user_id}'
        )