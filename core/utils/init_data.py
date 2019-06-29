# -*- coding: utf-8 -*-
from sqlalchemy import create_engine

from apps.people.generators.generate_people import PeopleFactory
from core.db import common
from core.utils.init_config import init_config
from core.utils.init_db import get_dsn


if __name__ == '__main__':
    config = init_config()
    dsn = get_dsn(config)

    engine = create_engine(dsn)
    common.Session.configure(bind=engine)
    session = common.Session()

    for i in range(config.RESOURCE_NUMBER_ELEMENTS):
        p = PeopleFactory()
        session.commit()
