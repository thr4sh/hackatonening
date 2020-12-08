"""
This is the people module and supports all the ReST actions for the
PEOPLE collection
"""

# System modules
from datetime import datetime
from models import Person, Note
# 3rd party modules
from flask import make_response, abort


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

from flask import (
  make_response,
  abort,
)
from config import db
from models import (
  Person,
  PersonSchema,
)

# Data to serve with our API
PEOPLE = {
    "Farrell": {
        "fname": "Doug",
        "lname": "Farrell",
        "timestamp": get_timestamp(),
    },
    "Brockman": {
        "fname": "Kent",
        "lname": "Brockman",
        "timestamp": get_timestamp(),
    },
    "Easter": {
        "fname": "Bunny",
        "lname": "Easter",
        "timestamp": get_timestamp(),
    },
}


def read_all():
    """
    This function responds to a request for /api/people
    with the complete lists of people
    :return:    json string of list of people
    """
    # Create the list of people from our data
    people = Person.query.order_by(Person.lname).all()
    # Serialize the data for the response
    person_schema = PersonSchema(many=True)
    return person_schema.dump(people)


def read_one(person_id):
    """
    Эта функция отвечает на запрос /api / people / {person_id}
    с одним подходящим человеком из людей

    :param person_id:   Id человека, которого нужно найти
    :return:            личность, совпадающая с идентификатором
    """
    # Постройте начальный запрос
    person = (
        Person.query.filter(Person.person_id == person_id)
            .outerjoin(Note)
            .one_or_none()
    )

    # Мы нашли человека?
    if person is not None:

        # Сериализуйте данные для ответа
        person_schema = PersonSchema()
        data = person_schema.dump(person)
        return data

    # В противном случае, нет, я не нашел этого человека
    else:
        abort(404, f"Person not found for Id: {person_id}")


def create(person):
    """
    This function creates a new person in the people structure
    based on the passed-in person data
    :param person: person to create in people structure
    :return:    201 on success, 406 on person exists
    """
    fname = person.get('fname')
    lname = person.get('lname')
    tm = person.get('timestamp')
    nt = person.get('notes')
    existing_person = Person.query \
        .filter(Person.fname == fname) \
        .filter(Person.lname == lname) \
        .one_or_none()
    # Can we insert this person?
    if existing_person is None:
        # Create a person instance using the schema and the passed-in person
        schema = PersonSchema()
        new_person = Person(lname = lname, fname = fname, timestamp = tm, notes = nt)
        # Add the person to the database
        db.session.add(new_person)
        db.session.commit()
        # Serialize and return the newly created person in the response
        return schema.dump(new_person).data, 201
    # Otherwise, nope, person exists already
    else:
        abort(409, f'Person {fname} {lname} exists already')


def update(person, person_id):
    """
    This function updates an existing person in the people structure
    :param lname:   last name of person to update in the people structure
    :param person:  person to update
    :return:        updated person structure
    """
    # Does the person exist in people?
    qperson = (
        Person.query.filter(Person.person_id == person_id)
            .outerjoin(Note)
            .one_or_none()
    )
    if qperson is not None:
        schema = PersonSchema()
        qperson.lname = person.get('lname')
        qperson.fname = person.get('fname')
        qperson.notes = person.get('notes')

        db.session.commit
        return schema.dump(qperson), 201
    else:
        abort(
            404, "Person with id {person_id} not found".format(person_id=person_id)
        )

    return person


def delete(person_id):
    """
    This function deletes a person from the people structure
    :param lname:   last name of person to delete
    :return:        200 on successful delete, 404 if not found
    """
    # Does the person to delete exist?
    qperson = (
        Person.query.filter(Person.person_id == person_id)
            .outerjoin(Note)
            .one_or_none()
    )
    if qperson is not None:
        db.session.delete(qperson)
        db.session.commit()

        return 200
    else:
        abort(
            404, "Person with id {person_id} not found".format(person_id=person_id))