# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import BaseModel


class PeopleSerializer(BaseModel):
    first_name: str
    last_name: str
    place_id: int
    is_king: bool = False
    is_alive: bool = True

    class Config:
        orm_mode = True


class PeopleOutSerializer(PeopleSerializer):
    id: int
    created: datetime
