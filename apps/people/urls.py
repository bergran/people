# -*- coding: utf-8 -*-

from fastapi.routing import APIRouter
from apps.people.views.people import router as people_router


router = APIRouter()
router.include_router(people_router, prefix='/people')
