from datetime import datetime
from flask import (
  make_response,
  abort,
)
from config import db
from models import (
  Person,
  PersonSchema,
  Note,
  NotePersonSchema,
  PersonNoteSchema,
  NoteSchema
)


def read_all(person_id):
    note = (
        Note.query.join(Person, Person.person_id == Note.person_id).filter(Person.person_id == person_id)
    )

    # Была ли найдена запись?
    if note is not None:
        print(f"Found something under an id of {person_id}")

        note_schema = NoteSchema(many = True)
        data = note_schema.dump(note)
        return data

    # В противном случае, нет, я не нашел эту запись
    else:
        abort(404, f"The following person does not contain any notes: {person_id}")

def read_one(person_id, note_id):
    """
    Эта функция отвечает на запрос о
    /api/people/{person_id}/notes/{note_id}
    с одной соответствующей note для связанного лица

    :param person_id:       Id of person the note is related to
    :param note_id:         Id of the note
    :return:                json string of note contents
    """
    # Запросите эту заметку в базе данных
    note = (
        Note.query.join(Person, Person.person_id == Note.person_id)
        .filter(Person.person_id == person_id)
        .filter(Note.note_id == note_id)
        .one_or_none()
    )

    # Была ли найдена запись?
    if note is not None:
        note_schema = NoteSchema()
        data = note_schema.dump(note)
        return data

    # В противном случае, нет, я не нашел эту запись
    else:
        abort(404, f"Note not found for Id: {note_id}")

def create(person_id, note):
    person = (
        Person.query.filter(Person.person_id == person_id)
            .outerjoin(Note)
            .one_or_none()
    )

    # Мы нашли человека?
    if person is not None:
        nnote = Note(person_id = person_id, content = note.get("content"))
        db.session.add(nnote)
        db.session.commit()
        note_schema = NoteSchema()
        data = note_schema.dump(nnote)
        return 200, data
    else:
        abort(404, f"The following person DOES NOT FUCKING EXIST: {person_id}")

def update(person_id, note_id, note):

    qnote = (
        Note.query.join(Person, Person.person_id == Note.person_id)
        .filter(Person.person_id == person_id)
        .filter(Note.note_id == note_id)
        .one_or_none()
    )

    # Была ли найдена запись?
    if qnote is not None:

        qnote.content = note
        db.session.commit

        note_schema = NoteSchema()
        data = note_schema.dump(qnote)
        return 200, data
    # В противном случае, нет, я не нашел эту запись
    else:
        abort(404, f"Note not found for note_id: {note_id} person_id: {person_id}")

def delete(person_id, note_id):

    qnote = (
        Note.query.join(Person, Person.person_id == Note.person_id)
        .filter(Person.person_id == person_id)
        .filter(Note.note_id == note_id)
        .one_or_none()
    )

    # Была ли найдена запись?
    if qnote is not None:

        db.session.delete(qnote)
        db.session.commit



        return 200
    # В противном случае, нет, я не нашел эту запись
    else:
        abort(404, f"Note not found for note_id: {note_id} person_id: {person_id}")
