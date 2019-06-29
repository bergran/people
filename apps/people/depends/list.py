# -*- coding: utf-8 -*-
from fastapi import Depends
from sqlalchemy.orm import Session

from apps.people.depends.filters import get_filters
from apps.people.depends.order_by import get_ordering
from apps.people.models import People
from core.depends import get_database


def get_queryset(
        session: Session = Depends(get_database),
        filters=Depends(get_filters),
        ordering=Depends(get_ordering)
):
    qs = session.query(People).filter(People.deleted_.is_(False))

    if filters is not None:
        qs = qs.filter(*filters)

    if ordering is not None:
        qs = qs.order_by(ordering)

    return qs
