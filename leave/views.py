from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from .models import CustomUser, LeaveBalance, LeaveType, LeaveRequest
from .serializers import LeaveBalanceSerializer, LeaveRequestSerializer, LeaveTypeSerializer, UserSerializer, RegisterSerializer, ProfileSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsEmployee, IsSuperUser, IsManager
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from django.utils.timezone import now

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


    def create(self, request, *args, **kwargs):
        print("request ===", request.data)
        return super().create(request, *args, **kwargs)
    



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

    def get_queryset(self):
        return CustomUser.objects.filter(id=self.request.user.id)




class LeaveRequestViewSet(ModelViewSet):
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializer
    permission_classes = [IsAuthenticated]


    def create(self, request, *args, **kwargs):
        print('1st req data = ', request.data)
        return super().create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        print("Validated data before saving:", serializer.validated_data)
        serializer.save(employee=self.request.user)


class LeaveTypeViewSet(ModelViewSet):
    queryset = LeaveType.objects.all()
    serializer_class = LeaveTypeSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        print('requested data ======', request.data)
        return super().create(request, *args, **kwargs)

class LeaveBalanceViewSet(ModelViewSet):
    queryset = LeaveBalance.objects.all()
    serializer_class = LeaveBalanceSerializer
    permission_classes = [IsAuthenticated]

