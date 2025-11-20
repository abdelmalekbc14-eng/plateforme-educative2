from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from accounts.views import (
    RegisterStudentView,
    MyTokenObtainPairView,
    MeView,
)

# Les urls de l'app accounts
urlpatterns = [
    
    path("register/", RegisterStudentView.as_view(), name="student-register"),
    path("login/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    
    # Endpoint user info
    path("me/", MeView.as_view(), name="me"), 
]
