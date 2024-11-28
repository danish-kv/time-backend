from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from .models import CustomUser, LeaveBalance, LeaveType, LeaveRequest
from .serializers import LeaveBalanceSerializer, LeaveRequestSerializer, LeaveTypeSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsEmployee, IsSuperUser, IsManager
from rest_framework_simplejwt.views import TokenObtainPairView


class UserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    # def get_permissions(self):
    #     if self.action in ['create']:
    #         return [IsManager()]
    #     return [IsAuthenticated()]

    # def get_queryset(self):
    #     user = self.request.user
    #     if user.role == 'manager':
    #         return CustomUser.objects.filter(manager=user)
    #     return super().get_queryset()
    



class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        print(request.data)
        res = super().post(request, *args, **kwargs)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user

        res.data['user'] = user.username
        res.data['user'] = user.id

        return res
    
    

class LeaveRequestViewSet(ModelViewSet):
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializer
    permission_classes = [IsAuthenticated]


class LeaveTypeViewSet(ModelViewSet):
    queryset = LeaveType.objects.all()
    serializer_class = LeaveTypeSerializer
    permission_classes = [IsAuthenticated]


class LeaveBalanceViewSet(ModelViewSet):
    queryset = LeaveBalance.objects.all()
    serializer_class = LeaveBalanceSerializer
    permission_classes = [IsAuthenticated]

