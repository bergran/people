# -*- coding: utf-8 -*-
from typing import List

from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session, Query
from starlette import status
from starlette.responses import UJSONResponse

from apps.people.depends.list import get_queryset
from apps.people.models.people import People
from apps.people.serializers.people import PeopleOutSerializer, PeopleSerializer
from apps.people.validators.people import validate_people, validate_people_update
from core.depends import get_database
from core.utils.get_object_or_404 import get_object_or_404

router = APIRouter()


@router.get('/', response_model=List[PeopleOutSerializer])
def list_people(qs: Query = Depends(get_queryset)):
    return qs.all()


@router.get('/{people_id}', response_model=PeopleOutSerializer)
async def retrieve_people(people_id: int, session: Session = Depends(get_database)):
    qs = session.query(People).filter(People.id == people_id, People.deleted_.is_(False))
    obj = get_object_or_404(qs)

    return obj


@router.post('/', response_model=PeopleOutSerializer, status_code=status.HTTP_201_CREATED)
def create_people(people: PeopleSerializer, session: Session = Depends(get_database)):
    obj = People()

    validate_people(obj, people, session)

    for name, value in people.dict().items():
        setattr(obj, name, value)

    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


@router.put('/{people_id}', response_model=PeopleOutSerializer)
def update_people(people_id: int, people: PeopleSerializer, session: Session = Depends(get_database)):
    qs = session.query(People).filter(People.id == people_id, People.deleted_.is_(False))
    obj = get_object_or_404(qs)

    validate_people_update(obj, people, session)

    for name, value in people.dict().items():
        setattr(obj, name, value)

    session.commit()
    session.refresh(obj)
    return obj


@router.delete('/{people_id}', response_model=PeopleOutSerializer, status_code=status.HTTP_204_NO_CONTENT)
async def delete_people(people_id: int, session: Session = Depends(get_database)):
    qs = session.query(People).filter(People.id == people_id, People.deleted_.is_(False))
    obj = get_object_or_404(qs)
    await perform_delete(obj, session)
    return UJSONResponse(status_code=status.HTTP_204_NO_CONTENT)


@router.delete('/place/{place_id}', response_model=PeopleOutSerializer, status_code=status.HTTP_204_NO_CONTENT)
async def delete_people_by_place(place_id: int, session: Session = Depends(get_database)):
    update_q = People.__table__.update().where(People.place_id == place_id).values({'deleted_': True})
    session.execute(update_q)
    session.commit()
    return UJSONResponse({}, status_code=status.HTTP_204_NO_CONTENT)


async def perform_delete(obj, session):
    obj.deleted_ = True
    session.commit()
    session.refresh(obj)
