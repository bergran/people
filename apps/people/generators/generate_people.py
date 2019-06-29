# -*- coding: utf-8 -*-
import random

import factory

from apps.people.models import People
from core import config
from core.db import common


class PeopleFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = People
        sqlalchemy_session = common.Session

    first_name = factory.Sequence(lambda n: u'User %d' % n)
    last_name = factory.Sequence(lambda n: u'User %d' % n)
    place_id = factory.Sequence(lambda n: random.randint(1, config.RESOURCE_PLACES_NUMBER_ELEMENTS))
