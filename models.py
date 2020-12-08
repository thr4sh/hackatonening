import sqlite3
from datetime import datetime
from config import db, ma
from marshmallow_sqlalchemy.fields import Nested, fields
from sqlalchemy.orm import relationship

class Level(db.Model):
    __tablename__ = 'level'
    id = db.Column('ID', db.String, primary_key = True, nullable = False)
    name = db.Column('NAME', db.String(200), nullable = False)

class Structure(db.Model):
    __tablename__ = 'structure'
    id = db.Column('ID', db.String, primary_key = True, nullable = False)
    name = db.Column('NAME', db.String(200), nullable = False)

class Faculty(db.Model):
    __tablename__ = 'faculty'
    id = db.Column('ID', db.String, primary_key = True, nullable = False)
    name = db.Column('NAME', db.String(200), nullable = False)

class Corpus(db.Model):
    __tablename__ = 'corpus'
    id = db.Column('ID', db.Strig, primary_key = True, nullable = False)
    name = db.Column('NAME', db.String(200), nullable = False)

class Group(db.Model):
    __tablename__ = 'group'
    id = db.Column('ID', db.String, primary_key = True, nullable = False)
    name = db.Column('NAME', db.String(50), nullable = False)
    course = db.Column('COURSE', db.String, nullable = False)
    url = db.Column('URL', db.String(200))
    id_faculty = db.Column('ID_FACULTY', db.String, db.ForeignKey('faculty.id'), nullable = False)
    id_structure = db.Column('ID_STRUCTURE', db.String, db.ForeignKey('structure.id'), nullable = False)
    id_level = db.Column('ID_LEVEL', db.String, db.ForeignKey('level.id'), nullable = False)
    child_fac = db.relationship("Faculty", backref= "Group")
    child_struc = db.relationship("Structure", backref="Group")
    child_lev = db.relationship("Level", backref="Group")

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column('ID', db.String, primary_key=True, nullable = False)
    name = db.Column('NAME', db.String(200), nullable = False)
    login = db.Column('LOGIN', db.String(200), nullable = False)
    password = db.Column('PASSWORD', db.String(200), nullable = False)
    token = db.Column('TOKEN', db.String(32), nullable = False)#IN db is stored as CHARACTER(32). Must consult docs on correct representation
    expiration = db.Column('EXPIRATION', db.DateTime, nullable = False)

class Log(db.Model):
    __tablename__ = 'user'
    id = db.Column('ID', db.String, primary_key=True, nullable=False)
    id_user = db.Column('ID_USER', db.String, db.ForeignKey('user.id'), nullable=True)
    method = db.Column('METHOD', db.String(6), nullable=False)
    url = db.Column('URL', db.String(200), nullable=False)
    status = db.Column('STATUS', db.String, nullable=False)
    ip = db.Column('IP', db.String(15), nullable=False)
    time = db.Column('TIME', db.DateTime, nullable=False)

    child_user = db.relationship("User", backref="Log")

class Auditory(db.Model):
    __tablename__ = 'auditory'
    id = db.Column('ID', db.String, primary_key=True, nullable=False)
    name = db.Column('USER', db.String(200), nullable=True)
    #should be a foreign key but it isnt wtf???
    id_corpus = db.Column('ID_CORPUS', db.String, nullable=False)

class Day(db.Model):
    __tablename__ = 'day'
    id = db.Column('ID', db.String, primary_key = True, nullable = False)
    name = db.Column('NAME', db.String(50), nullable = False)
    short = db.Column('SHORT', db.String(50), nullable=False)

class Lesson(db.Model):
    __tablename__ = 'lesson'
    id = db.Column('ID', db.String, primary_key = True, nullable = False)
    name = db.Column('NAME', db.String(200), nullable = False)

class Teacher(db.Model):
    __tablename__ = 'teacher'
    id = db.Column('ID', db.String, primary_key = True, nullable = False)
    name = db.Column('NAME', db.String(200), nullable = False)

class Teacher(db.Model):
    __tablename__ = 'time'
    id = db.Column('ID', db.String, primary_key = True, nullable = False)
    beg = db.Column('BEG', db.DateTime, nullable = False)
    end = db.Column('END', db.DateTime, nullable = False)

    children = db.relationship(
        "Schedule",
        secondary="TeacherSchedule",
        back_populates="Teacher")

class Schedule(db.Model):
    __tablename__ = 'schedule'
    id = db.Column('ID', db.String, primary_key=True, nullable=False)
    id_lesson = db.Column('ID_LESSON', db.String, db.ForeignKey('lesson.id'), nullable=False)
    id_day = db.Column('ID_DAY', db.String, nullable=False)
    id_group = db.Column('ID_GROUP', db.String, nullable=False)
    id_auditory = db.Column('ID_AUDITORY', db.String, nullable=False)
    id_time = db.Column('ID_TIME', db.String, nullable=False)
    week = db.Column('WEEK', db.String(1000), nullable=True)

    children = db.relationship(
        "Teacher",
        secondary="TeacherSchedule",
        back_populates="Schedule")

class TeacherSchedule(db.Model):
    __tablename__ = 'teacher_schedule'
    id_teacher = db.Column('ID_TEACHER', db.String, db.ForeignKey('lesson.id'), nullable=False)
    id_schedule = db.Column('ID_SCHEDULE', db.String, db.ForeignKey('lesson.id'), nullable=False)

#schemas start here

class Person(db.Model):
    __tablename__ = 'person'
    person_id = db.Column(db.Integer, primary_key=True)
    lname = db.Column(db.String(32))
    fname = db.Column(db.String(32))
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    notes = db.relationship(
        'Note',
        backref='person',
        cascade='all, delete, delete-orphan',
        single_parent=True,
        order_by='desc(Note.timestamp)'
    )


class Note(db.Model):
    __tablename__ = 'note'
    note_id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.person_id'))
    content = db.Column(db.String, nullable=False)
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

#ModelSchema --> SQLAlchemyAutoSchema in new versions
class PersonSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Person
        sqla_session = db.session
        include_relationships = True
        load_instance = True
    notes = Nested('PersonNoteSchema', default=[], many=True)

class PersonNoteSchema(ma.SQLAlchemyAutoSchema):
    """
    This class exists to get around a recursion issue
    """
    note_id = fields.Int()
    person_id = fields.Int()
    content = fields.Str()
    timestamp = fields.Str()

class NoteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Note
        sqla_session = db.session
        include_relationships = True
        load_instance = True

    note_id = fields.Int()
    person_id = fields.Int()
    content = fields.Str()
    timestamp = fields.Str()

    person = Nested('NotePersonSchema', default=None)

class NotePersonSchema(ma.SQLAlchemyAutoSchema):
    """
    Этот класс существует, чтобы обойти проблему рекурсии
    """
    person_id = fields.Int()
    lname = fields.Str()
    fname = fields.Str()
    timestamp = fields.Str()
