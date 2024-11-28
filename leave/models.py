from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICE = (
        ("employee", "Employee"),
        ("manager", "Manager"),
    )
    role = models.CharField(choices=ROLE_CHOICE, max_length=10, default="employee")
    department = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self) -> str:
        return self.username


class LeaveType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


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
    status = models.CharField(choices=STATUS_CHOICES, max_length=10, default="pending")
    manager = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="managed_requests")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.username} - {self.leave_type.name} - {self.status}"

    class Meta:
        ordering = ["-created_at"]  


class LeaveBalance(models.Model): 
    employee = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    total_leaves = models.IntegerField(default=0)
    used_leaves = models.IntegerField(default=0)

    @property
    def remaining_leaves(self):
        return self.total_leaves - self.used_leaves

    def __str__(self):
        return f"{self.employee.username} - {self.leave_type.name}"