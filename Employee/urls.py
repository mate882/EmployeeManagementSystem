from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Employee URLs
    path('employees/', views.EmployeeListView.as_view(), name='employee_list'),
    path('employees/add/', views.EmployeeCreateView.as_view(), name='employee_add'),
    path('employees/<int:pk>/', views.employee_detail, name='employee_detail'),
    path('employees/<int:pk>/edit/', views.EmployeeUpdateView.as_view(), name='employee_edit'),
    
    # Department URLs
    path('departments/', views.DepartmentListView.as_view(), name='department_list'),
    path('departments/add/', views.DepartmentCreateView.as_view(), name='department_add'),
    path('departments/<int:pk>/edit/', views.DepartmentUpdateView.as_view(), name='department_edit'),
    
    # Job Title URLs
    path('job-titles/', views.JobTitleListView.as_view(), name='jobtitle_list'),
    path('job-titles/add/', views.JobTitleCreateView.as_view(), name='jobtitle_add'),
    path('job-titles/<int:pk>/edit/', views.JobTitleUpdateView.as_view(), name='jobtitle_edit'),
    
    # Attendance URLs
    path('attendance/', views.AttendanceListView.as_view(), name='attendance_list'),
    path('attendance/add/', views.AttendanceCreateView.as_view(), name='attendance_add'),
    path('attendance/<int:pk>/edit/', views.AttendanceUpdateView.as_view(), name='attendance_edit'),
    
    # Promotion URLs
    path('promotions/', views.PromotionListView.as_view(), name='promotion_list'),
    path('promotions/promote/', views.promote_employee, name='promote_employee'),
    
    # AJAX URLs
    path('api/job-titles/<int:department_id>/', views.get_job_titles_by_department, name='job_titles_by_department'),
]
