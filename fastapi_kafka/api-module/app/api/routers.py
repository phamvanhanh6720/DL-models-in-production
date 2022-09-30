from fastapi import APIRouter
from .v1.resources import dl_router, show_image

router_v1 = APIRouter()

router_v1.include_router(dl_router.router, prefix="/model", tags=["Async API"])
router_v1.include_router(show_image.router, tags=["Async API"])



