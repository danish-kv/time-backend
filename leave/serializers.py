from rest_framework.serializers import ModelSerializer
from .models import CustomUser, LeaveRequest, LeaveType
from rest_framework import serializers




class RegisterSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email', 'department', 'first_name', 'last_name', 'date_joined']

    def create(self, validate_data):
        print('validate data ===',validate_data)
        password = validate_data.pop('password', '')
        user = CustomUser(**validate_data)

        user.set_password(password)
        user.save()

        return user

class UserSerializer(ModelSerializer):
    class Meta:
        fields = ['id', 'username', 'email', 'last_login', 'department', 'is_active', 'first_name', 'last_name']
        model = CustomUser



class ProfileSerializer(ModelSerializer):
    class Meta:
        fields = ['username', 'email', 'last_login', 'department', 'phone', 'location', 'date_joined']
        model = CustomUser


class LeaveTypeSerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        model = LeaveType


    def create(self, validated_data):
        print('validate data =====', validated_data)
        return super().create(validated_data)


class LeaveRequestSerializer(ModelSerializer):
    employee = UserSerializer(read_only = True)
    leave_type_detail = LeaveTypeSerializer(source='leave_type', read_only=True) 
    leave_type = serializers.PrimaryKeyRelatedField(queryset=LeaveType.objects.all())
    class Meta:
        fields = [ 'id', 'employee', 'leave_type', 'leave_type_detail', 'start_date', 'end_date', 'reason', 
                  'attachment', 'status', 'created_at', 'comment' ]
        model = LeaveRequest


