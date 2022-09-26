from fastapi import APIRouter
from .resources.v1 import show_image
from .resources.v1.model import dl_router


router_v1 = APIRouter()

router_v1.include_router(dl_router.router, prefix="/model",  tags=["API-V1"])
router_v1.include_router(show_image.router, prefix="/show-image",  tags=["API-V1"])



