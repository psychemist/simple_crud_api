#!/usr/bin/env python3
"""Module of User views
"""
from api.v2.views import app_views
from flask import abort, jsonify, make_response, request
from models.person import db, Person

from markupsafe import escape
from typing import Union


@app_views.route('/', methods=['GET'], strict_slashes=False)
def view_persons() -> str:
    """ GET /api
    Return:
      - List of all Person objects JSON represented
    """
    person_list = db.session.execute(
                 db.select(Person).order_by(Person.id)).scalars()
    persons = [person for person in person_list]
    return make_response(jsonify(persons), 200)


@app_views.route('/<user_id>', methods=['GET'], strict_slashes=False)
def view_person_by_id(user_id: Union[int, str]) -> str:
    """ GET /api/user_id
    Path parameter:
      - Person ID
    Return:
      - Person object JSON represented
      - 404 if Person ID does not exist
    """
    if Person.validate_name(user_id):
        person = Person.query.filter_by(name=user_id).first()
    if not person:
        if Person.validate_id(user_id):
            person = db.get_or_404(Person, user_id,
                                   description="User not found")
        else:
            abort(404,
                  description="UID must be a positive integer or valid string")
    return make_response(jsonify(person), 200)


@app_views.route('/', methods=['POST'], strict_slashes=False)
def create_person() -> str:
    """ POST /api
    JSON body:
      - name
    Return:
      - Person object JSON represented
      - 400 if unable to create Person
    """
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    name = request.get_json().get('name')
    if not Person.validate_name(name):
        abort(400, description="Name must be a string")

    person = Person(name=escape(name))
    db.session.add(person)
    db.session.commit()
    return make_response(jsonify(person), 201)


@app_views.route('/<user_id>', methods=['PUT'], strict_slashes=False)
def update_person(user_id: Union[int, str]) -> str:
    """ PUT /api/user_id
    Path parameter:
      - Person ID
    JSON body:
      - name
    Return:
      - User object JSON represented
      - 400 if unable to update Person
      - 404 if Person ID does not exist
    """
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    name = request.get_json().get('name')
    if not Person.validate_name(name):
        abort(400, description="Name must be a string")

    if Person.validate_name(user_id):
        person = Person.query.filter_by(name=user_id).first()
    if not person:
        if Person.validate_id(user_id):
            person = db.get_or_404(Person, user_id,
                                   description="User not found")
        else:
            abort(404,
                  description="UID must be a positive integer or valid string")

    person.name = escape(name)
    db.session.commit()
    return make_response(jsonify(person), 200)


@app_views.route('/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_person(user_id: Union[int, str]):
    """ DELETE /api/user_id
    Path parameter:
      - Person ID
    Return:
      - Empty JSON if Person object has been correctly deleted
      - 400 if unable to delete Person
      - 404 if Person ID does not exist
    """
    if Person.validate_name(user_id):
        person = Person.query.filter_by(name=user_id).first()
    if not person:
        if Person.validate_id(user_id):
            person = db.get_or_404(Person, user_id,
                                   description="User not found")
        else:
            abort(404,
                  description="UID must be a positive integer or valid string")
    db.session.delete(person)
    db.session.commit()
    return make_response(jsonify({}), 204)
