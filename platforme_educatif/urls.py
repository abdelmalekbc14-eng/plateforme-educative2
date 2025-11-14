from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/auth/", include("accounts.urls")),
    path("api/cours/", include("cours.urls")),
    path("api/timetable/", include("timetable.urls")),
    path("api/messaging/", include("messaging.urls")),

    # Frontend
    path("", include("frontend.urls")),
    path("", include("service_discovery.urls")),
]
