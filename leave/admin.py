from django.contrib import admin
from .models import CustomUser, LeaveType, LeaveRequest

admin.site.register(CustomUser)
admin.site.register(LeaveType)
admin.site.register(LeaveRequest)
