from django.db import models
from centers.models import center

class Employee(models.Model):
    code = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    daily_salary = models.DecimalField(max_digits=10, decimal_places=2)
    center = models.ForeignKey(center, on_delete=models.CASCADE)  # If center represents centers

    def __str__(self):
        return self.name

class EmployeeAttendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    presence_status = models.BooleanField(default=True)  # True for present, False for absent
    massrouf = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.employee.name} - {self.date}"
