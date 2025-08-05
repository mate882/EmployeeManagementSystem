from django import forms
from .models import Employee, Department, JobTitle, AttendanceRecord, PromotionHistory
from django.contrib.auth.models import User

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['employee_id', 'first_name', 'last_name', 'email', 'phone', 'address', 
                 'date_of_birth', 'gender', 'department', 'job_title', 'hire_date', 
                 'salary', 'status', 'manager']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'hire_date': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
            'salary': forms.NumberInput(attrs={'step': '0.01'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['manager'].queryset = Employee.objects.filter(status='active')

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class JobTitleForm(forms.ModelForm):
    class Meta:
        model = JobTitle
        fields = ['title', 'department', 'base_salary']
        widgets = {
            'base_salary': forms.NumberInput(attrs={'step': '0.01'}),
        }

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = AttendanceRecord
        fields = ['employee', 'date', 'clock_in', 'clock_out', 'break_minutes', 'status', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'clock_in': forms.TimeInput(attrs={'type': 'time'}),
            'clock_out': forms.TimeInput(attrs={'type': 'time'}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }

class PromotionForm(forms.ModelForm):
    class Meta:
        model = PromotionHistory
        fields = ['employee', 'new_job_title', 'new_department', 'new_salary', 'promotion_date', 'reason']
        widgets = {
            'promotion_date': forms.DateInput(attrs={'type': 'date'}),
            'new_salary': forms.NumberInput(attrs={'step': '0.01'}),
            'reason': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['employee'].queryset = Employee.objects.filter(status='active')
