from rest_framework.serializers import ModelSerializer
from .models import CustomUser, LeaveBalance, LeaveRequest, LeaveType
from rest_framework import serializers



class UserSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        fields = ['username', 'department', 'password']
        model = CustomUser


class LeaveTypeSerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        model = LeaveType


class LeaveRequestSerializer(ModelSerializer):
    employee = UserSerializer(read_only = True)
    leave_type = LeaveTypeSerializer()
    class Meta:
        fields = '__all__'
        model = LeaveRequest


class LeaveBalanceSerializer(ModelSerializer):
    employee = UserSerializer(read_only = True)
    class Meta:
        fields = '__all__'
        model = LeaveBalance

