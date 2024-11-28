from django.contrib import admin
from .models import CustomUser, LeaveType, LeaveRequest, LeaveBalance

admin.site.register(CustomUser)
admin.site.register(LeaveType)
admin.site.register(LeaveRequest)
admin.site.register(LeaveBalance)
