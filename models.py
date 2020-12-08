import sqlite3
from datetime import datetime
from config import db, ma
from marshmallow_sqlalchemy.fields import Nested, fields

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
