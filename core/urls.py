# -*- coding: utf-8 -*-

from fastapi.routing import APIRouter

from apps.health_check.urls import router as router_health_check
from apps.people.urls import router as router_people_check


router = APIRouter()
router.include_router(router_health_check, prefix='/api/v1')
router.include_router(router_people_check, prefix='/api/v1')
