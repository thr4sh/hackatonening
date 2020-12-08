#WHEN GETTING HIGH ISN'T ENOUGH
from datetime import datetime, timedelta, date
from models import (User, UserSchema, Faculty, FacultySchema, Teacher, TeacherSchema, Schedule, ScheduleSchema,
                    AuditorySchema, Auditory, Group, GroupScheme, Structure, StructureSchema, LevelSchema, Level)
from flask import (make_response, abort)
from config import db
from valid import gen_token, valid
from logdb import log_access

def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


def read_facs_all(token):
    if not valid(token):
        log_access(token, 403)
        abort(403, 'Phony token detected')

    sc = Faculty.query.order_by(Faculty.id).all()
    s = FacultySchema(many = True)
    if sc is not None:
        log_access(token, 200)
        return s.dump(sc)
    else:
        log_access(token, 404)
        abort(404, "Not found")

def read_teachers(token):
    if not valid(token):
        log_access(token, 403)
        abort(403, 'Phony token detected')

    sc = Teacher.query.order_by(Teacher.id).all()
    s = TeacherSchema(many = True)
    if sc is not None:
        log_access(token, 200)
        return s.dump(sc)
    else:
        log_access(token, 404)
        abort(404, "Not found")

def read_auds(token):
    if not valid(token):
        log_access(token, 403)
        abort(403, 'Phony token detected')

    sc = Auditory.query.order_by(Auditory.id).all()
    s = AuditorySchema(many = True)
    if sc is not None:
        log_access(token, 200)
        return s.dump(sc)
    else:
        log_access(token, 404)
        abort(404, "Not found")


def read_fac(token, faculty_id):

    if not valid(token):
        #log_access(token, 403)
        abort(403, 'Phony token detected')

    sc = Faculty.query.filter(Faculty.id == faculty_id).one_or_none()
    if sc is not None:
        s = FacultySchema().dump(sc)
        gp = Group.query.filter(Group.id_faculty == faculty_id).all()
        #unique set (Group.id_structure, Group.id_level)
        dc = {}
        for g in gp:
            if str(g.id_structure) not in dc:
                dc[str(g.id_structure)] = set()

            dc[str(g.id_structure)].add(str(g.id_level))

        #hell
        s['structures'] = []
        for d in dc:
            s['structures'].append(StructureSchema.dump(Structure.query.filter(Structure.id == d[0]).one_or_none()))
            s['structures'][-1]['levels'] = []
            for s in d[1]:
                s['structures'][-1]['levels'].append(LevelSchema().dump(Level.query.filter(Level.id == s).one_or_none()))
                s['structures'][-1]['levels'][-1]['groups'] = GroupScheme().dump(Group.query.filter(Group.id_level == s).all)

        #log_access(token, 200)
        return s
    else:
        #log_access(token, 404)
        abort(404, "Not found")


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
