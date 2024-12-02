from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    profile = models.ImageField(upload_to='profile/', null=True)
    role = models.CharField(max_length=10, default="employee")
    phone = models.IntegerField(null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self) -> str:
        return self.username
    
    class Meta:
        ordering = ['-id']


class LeaveType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-id']


class LeaveRequest(models.Model): 
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    )
    employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="leave_requests")
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE, related_name="leave_requests")
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    attachment = models.FileField(upload_to='attachment/', blank=True,null=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=10, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(null=True)

    def __str__(self):
        return f"{self.employee.username} - {self.leave_type.name} - {self.status}"

    class Meta:
        ordering = ["-created_at"]  


