from django.contrib import admin
from .models import Department, JobTitle, Employee, AttendanceRecord, PromotionHistory

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    list_filter = ['created_at']

@admin.register(JobTitle)  
class JobTitleAdmin(admin.ModelAdmin):
    list_display = ['title', 'department', 'base_salary', 'created_at']
    list_filter = ['department', 'created_at']
    search_fields = ['title']

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'full_name', 'department', 'job_title', 'status', 'hire_date']
    list_filter = ['status', 'department', 'job_title', 'gender']
    search_fields = ['employee_id', 'first_name', 'last_name', 'email']
    date_hierarchy = 'hire_date'
    list_per_page = 25
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('employee_id', 'first_name', 'last_name', 'email', 'phone')
        }),
        ('Personal Details', {
            'fields': ('date_of_birth', 'gender', 'address')
        }),
        ('Employment Details', {
            'fields': ('department', 'job_title', 'hire_date', 'salary', 'status', 'manager')
        }),
    )

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ['employee', 'date', 'clock_in', 'clock_out', 'hours_worked', 'status']
    list_filter = ['status', 'date', 'employee__department']
    search_fields = ['employee__first_name', 'employee__last_name', 'employee__employee_id']
    date_hierarchy = 'date'
    list_per_page = 30

@admin.register(PromotionHistory)
class PromotionHistoryAdmin(admin.ModelAdmin):
    list_display = ['employee', 'promotion_date', 'previous_job_title', 'new_job_title', 'new_salary']
    list_filter = ['promotion_date', 'new_department', 'approved_by']
    search_fields = ['employee__first_name', 'employee__last_name']
    date_hierarchy = 'promotion_date'
    readonly_fields = ['approved_by', 'created_at']