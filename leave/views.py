from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, filters
from rest_framework.viewsets import ModelViewSet
from .models import CustomUser, LeaveType, LeaveRequest
from .serializers import LeaveRequestSerializer, LeaveTypeSerializer, UserSerializer, RegisterSerializer, ProfileSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsEmployee, IsManager
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from django.utils.timezone import now
from django_filters.rest_framework import DjangoFilterBackend





class UserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['email', 'username']

    def get_permissions(self):
        if self.action in ['create']:
            return [IsManager()]
        return [IsAuthenticated()]

    def get_queryset(self):
        return CustomUser.objects.all().exclude(is_superuser=True)



class RegisterAPIView(APIView):
    permission_classes=[AllowAny]

    def post(self, request):
        data=request.data
        print('request data ===', data)
        serializer = RegisterSerializer(data=data)

        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error' : str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        print(request.data)
        res = super().post(request, *args, **kwargs)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user

        user.last_login = now()
        user.save(update_fields=['last_login'])

        res.data['user'] = user.username
        res.data['userID'] = user.id
        res.data['role'] = 'manager' if user.is_superuser else 'employee'

        return res
    


class Logout(APIView):
    def post(self, request):
        try:
            refresh = request.data.get('refresh')
            if not refresh:
                return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh)
            token.blacklist()

            return Response({"detail": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)

        except TokenError as e:
            return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class ProfileViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsEmployee]

    def get_queryset(self):
        return CustomUser.objects.filter(id=self.request.user.id)




class LeaveRequestViewSet(ModelViewSet):
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'leave_type__name']

    
    def perform_create(self, serializer):
        serializer.save(employee=self.request.user)

    def get_queryset(self):
        user = self.request.user
        queryset = LeaveRequest.objects.all()

        if not user.is_superuser:
            queryset = queryset.filter(employee=user)
        return queryset
    

class LeaveTypeViewSet(ModelViewSet):
    queryset = LeaveType.objects.all()
    serializer_class = LeaveTypeSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        print('requested data ======', request.data)
        return super().create(request, *args, **kwargs)



class DashboardAPIView(APIView):
    permission_classes = [IsManager]

    def get(self,request):
        total_employees = CustomUser.objects.count()
        total_pending = LeaveRequest.objects.filter(status='pending').count()
        total_approved = LeaveRequest.objects.filter(status='approved').count()
        total_rejected = LeaveRequest.objects.filter(status='rejected').count()
        
        last_three_pending = LeaveRequest.objects.filter(status='pending').order_by('-created_at')[:3]

        serializer = LeaveRequestSerializer(last_three_pending, many=True)

        stats = {
            'total_employees' : total_employees,
            'total_pending' : total_pending,
            'total_approved' : total_approved,
            'total_rejected' : total_rejected,
        }

        data = {
            "stats" : stats,
            'last_three_pending' : serializer.data
        }


        return Response(data=data)
