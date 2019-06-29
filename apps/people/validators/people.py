# -*- coding: utf-8 -*-
from fastapi import HTTPException
from sqlalchemy.sql.functions import count
from starlette import status

from apps.people.models import People


def validate_place_kings(obj, people, session):
    count_people = session.query(count(People.id)).filter(
        People.is_king.is_(True),
        People.is_alive.is_(True),
        People.place_id == people.place_id
    ).scalar()

    if people.is_king and people.is_alive and count_people != 0:
        detail = 'It can not be 2 kings alive in the same place'
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


def validate_place_kings_updated(obj, people, session):
    count_people = session.query(count(People.id)).filter(
        People.is_king.is_(True),
        People.is_alive.is_(True),
        People.place_id == people.place_id,
        People.id != obj.id
    ).scalar()

    if people.is_king and people.is_alive and count_people != 0:
        detail = 'It can not be 2 kings alive in the same place'
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


def validate_first_name(obj, people, session):
    count_people = session.query(count(People.id)).filter(
        People.first_name == people.first_name
    ).scalar()

    if count_people > 0:
        detail = 'It can not be 2 people with the same first name'
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


def validate_people(obj, people, session):
    validate_first_name(obj, people, session)
    validate_place_kings(obj, people, session)


def validate_people_update(obj, people, session):
    validate_first_name(obj, people, session)
    validate_place_kings_updated(obj, people, session)
