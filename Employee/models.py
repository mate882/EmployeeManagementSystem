from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class JobTitle(models.Model):
    title = models.CharField(max_length=100, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='job_titles')
    base_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.department.name}"
    
    class Meta:
        ordering = ['title']

class Employee(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('terminated', 'Terminated'),
    ]
    
    employee_id = models.CharField(max_length=20, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    job_title = models.ForeignKey(JobTitle, on_delete=models.SET_NULL, null=True)
    hire_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    manager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.employee_id})"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        ordering = ['last_name', 'first_name']

class AttendanceRecord(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    clock_in = models.TimeField(null=True, blank=True)
    clock_out = models.TimeField(null=True, blank=True)
    break_minutes = models.IntegerField(default=0)
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    overtime_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=[
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('partial', 'Partial Day'),
        ('sick', 'Sick Leave'),
        ('vacation', 'Vacation'),
    ], default='present')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if self.clock_in and self.clock_out:
            from datetime import datetime, timedelta
            clock_in_dt = datetime.combine(self.date, self.clock_in)
            clock_out_dt = datetime.combine(self.date, self.clock_out)
            if clock_out_dt < clock_in_dt:
                clock_out_dt += timedelta(days=1)
            
            total_minutes = (clock_out_dt - clock_in_dt).total_seconds() / 60
            worked_minutes = total_minutes - self.break_minutes
            self.hours_worked = Decimal(str(worked_minutes / 60))
            
            if self.hours_worked > 8:
                self.overtime_hours = self.hours_worked - 8
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.employee.full_name} - {self.date}"
    
    class Meta:
        unique_together = ['employee', 'date']
        ordering = ['-date']

class PromotionHistory(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='promotion_history')
    previous_job_title = models.ForeignKey(JobTitle, on_delete=models.SET_NULL, null=True, related_name='previous_promotions')
    new_job_title = models.ForeignKey(JobTitle, on_delete=models.SET_NULL, null=True, related_name='new_promotions')
    previous_department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='previous_dept_promotions')
    new_department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='new_dept_promotions')
    previous_salary = models.DecimalField(max_digits=10, decimal_places=2)
    new_salary = models.DecimalField(max_digits=10, decimal_places=2)
    promotion_date = models.DateField()
    reason = models.TextField()
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.employee.full_name} - {self.promotion_date}"
    
    class Meta:
        ordering = ['-promotion_date']