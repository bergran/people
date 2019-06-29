# -*- coding: utf-8 -*-

import sqlalchemy
from sqlalchemy.sql.functions import now

from core.db.base import Base


class People(Base):
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    first_name = sqlalchemy.Column(sqlalchemy.String(40))
    last_name = sqlalchemy.Column(sqlalchemy.String(40))
    created = sqlalchemy.Column(sqlalchemy.DateTime, default=now())
    place_id = sqlalchemy.Column(sqlalchemy.Integer)
    is_king = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    is_alive = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    deleted_ = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
