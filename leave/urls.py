from django.urls import path, include
from .views import CustomUser, UserViewSet, LeaveRequestViewSet,LeaveBalanceViewSet, LeaveTypeViewSet, CustomTokenObtainPairView
from rest_framework.routers import DefaultRouter

routers = DefaultRouter()

routers.register('users', UserViewSet, basename='users')
routers.register('leave-request', LeaveRequestViewSet, basename='leave-request')
routers.register('leave-balance', LeaveBalanceViewSet, basename='leave-balance')
routers.register('leave-type', LeaveTypeViewSet, basename='leave-type')


urlpatterns = [
    path('', include(routers.urls)),
    path('token/', CustomTokenObtainPairView.as_view(), name='token')
]
