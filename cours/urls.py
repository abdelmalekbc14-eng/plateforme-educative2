# cours/urls.py
from rest_framework.routers import DefaultRouter
from .views import CoursViewSet, InscriptionViewSet

router = DefaultRouter()

# /api/cours/inscriptions/
router.register(r"inscriptions", InscriptionViewSet, basename="inscription")

# /api/cours/
router.register("", CoursViewSet, basename="cours")

urlpatterns = router.urls
