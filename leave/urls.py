from django.urls import path, include
from .views import  UserViewSet, LeaveRequestViewSet, LeaveTypeViewSet, CustomTokenObtainPairView, RegisterAPIView, ProfileViewSet, Logout, DashboardAPIView
from rest_framework.routers import DefaultRouter

routers = DefaultRouter()

routers.register('users', UserViewSet, basename='users')
routers.register('leave-request', LeaveRequestViewSet, basename='leave-request')
routers.register('leave-type', LeaveTypeViewSet, basename='leave-type')
routers.register('profile', ProfileViewSet, basename='profile')


urlpatterns = [
    path('', include(routers.urls)),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/token/', CustomTokenObtainPairView.as_view(), name='token'),
    path('logout/', Logout.as_view(), name='logout'),
    path('dashboard/', DashboardAPIView.as_view(), name='dashboard'),
]
