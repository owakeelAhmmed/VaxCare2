from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, ProfileView, ChangePasswordView, DoctorListView

urlpatterns = [
    # path('register/', RegisterView.as_view(), name='register'),
    # path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('profile/', ProfileView.as_view(), name='profile'),
    # path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('doctors/', DoctorListView.as_view(), name='doctor_list'),
]
