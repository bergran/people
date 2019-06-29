# -*- coding: utf-8 -*-
from fastapi import Query

from apps.people.models import People

ORDERING_CHOICES = {
    '-place': People.place_id.desc(),
    'place': People.place_id.asc()
}


def get_ordering(ordering: str = Query(None, max_length = 6)):
    return ORDERING_CHOICES.get(ordering)
