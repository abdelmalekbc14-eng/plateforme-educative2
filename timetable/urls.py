from rest_framework.routers import DefaultRouter
from .views import SeanceViewSet

router = DefaultRouter()
router.register("seances", SeanceViewSet, basename="seance")

urlpatterns = router.urls
