__all__ = ("router",)

from .details_views import router as detail_router
from .list_views import router

router.include_router(detail_router)
