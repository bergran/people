# -*- coding: utf-8 -*-
from typing import List
from fastapi import Depends

from apps.people.models import People
from core.depends.get_multiples_values_query import get_multiple_integer_values_query


def get_filters(
        people_ids: List[int] = Depends(get_multiple_integer_values_query('people_ids')),
        places_id: List[int] = Depends(get_multiple_integer_values_query('places_id'))
):
    filters = []

    if people_ids:
        filters.append(People.id.in_(people_ids))

    if places_id:
        filters.append(People.place_id.in_(places_id))

    return filters
