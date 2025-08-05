from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q, Avg
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Employee, Department, JobTitle, AttendanceRecord, PromotionHistory
from .forms import EmployeeForm, DepartmentForm, JobTitleForm, AttendanceForm, PromotionForm
import json
from datetime import date, datetime, timedelta

def dashboard(request):
    total_employees = Employee.objects.filter(status='active').count()
    total_departments = Department.objects.count()
    today_attendance = AttendanceRecord.objects.filter(date=date.today()).count()
    avg_salary = Employee.objects.filter(status='active').aggregate(Avg('salary'))['salary__avg'] or 0
    
    recent_employees = Employee.objects.filter(status='active').order_by('-created_at')[:5]
    recent_promotions = PromotionHistory.objects.order_by('-promotion_date')[:5]
    
    context = {
        'total_employees': total_employees,
        'total_departments': total_departments,
        'today_attendance': today_attendance,
        'avg_salary': avg_salary,
        'recent_employees': recent_employees,
        'recent_promotions': recent_promotions,
    }
    return render(request, 'employees/dashboard.html', context)

# Employee Views
class EmployeeListView(ListView):
    model = Employee
    template_name = 'employees/employee_list.html'
    context_object_name = 'employees'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Employee.objects.all()
        search = self.request.GET.get('search')
        department = self.request.GET.get('department')
        status = self.request.GET.get('status')
        
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(employee_id__icontains=search) |
                Q(email__icontains=search)
            )
        if department:
            queryset = queryset.filter(department_id=department)
        if status:
            queryset = queryset.filter(status=status)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departments'] = Department.objects.all()
        context['status_choices'] = Employee.STATUS_CHOICES
        return context

class EmployeeCreateView(CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employees/employee_form.html'
    success_url = reverse_lazy('employee_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Employee created successfully!')
        return super().form_valid(form)

class EmployeeUpdateView(UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employees/employee_form.html'
    success_url = reverse_lazy('employee_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Employee updated successfully!')
        return super().form_valid(form)

def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    recent_attendance = AttendanceRecord.objects.filter(employee=employee).order_by('-date')[:10]
    promotion_history = PromotionHistory.objects.filter(employee=employee).order_by('-promotion_date')
    
    context = {
        'employee': employee,
        'recent_attendance': recent_attendance,
        'promotion_history': promotion_history,
    }
    return render(request, 'employees/employee_detail.html', context)

# Department Views
class DepartmentListView(ListView):
    model = Department
    template_name = 'employees/department_list.html'
    context_object_name = 'departments'

class DepartmentCreateView(CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'employees/department_form.html'
    success_url = reverse_lazy('department_list')

class DepartmentUpdateView(UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'employees/department_form.html'
    success_url = reverse_lazy('department_list')

# Job Title Views
class JobTitleListView(ListView):
    model = JobTitle
    template_name = 'employees/jobtitle_list.html'
    context_object_name = 'job_titles'

class JobTitleCreateView(CreateView):
    model = JobTitle
    form_class = JobTitleForm
    template_name = 'employees/jobtitle_form.html'
    success_url = reverse_lazy('jobtitle_list')

class JobTitleUpdateView(UpdateView):
    model = JobTitle
    form_class = JobTitleForm
    template_name = 'employees/jobtitle_form.html'
    success_url = reverse_lazy('jobtitle_list')

# Attendance Views
class AttendanceListView(ListView):
    model = AttendanceRecord
    template_name = 'employees/attendance_list.html'
    context_object_name = 'attendance_records'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = AttendanceRecord.objects.all()
        employee = self.request.GET.get('employee')
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        
        if employee:
            queryset = queryset.filter(employee_id=employee)
        if date_from:
            queryset = queryset.filter(date__gte=date_from)
        if date_to:
            queryset = queryset.filter(date__lte=date_to)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employees'] = Employee.objects.filter(status='active')
        return context

class AttendanceCreateView(CreateView):
    model = AttendanceRecord
    form_class = AttendanceForm
    template_name = 'employees/attendance_form.html'
    success_url = reverse_lazy('attendance_list')

class AttendanceUpdateView(UpdateView):
    model = AttendanceRecord
    form_class = AttendanceForm
    template_name = 'employees/attendance_form.html'
    success_url = reverse_lazy('attendance_list')

# Promotion Views
class PromotionListView(ListView):
    model = PromotionHistory
    template_name = 'employees/promotion_list.html'
    context_object_name = 'promotions'
    paginate_by = 20

def promote_employee(request):
    if request.method == 'POST':
        form = PromotionForm(request.POST)
        if form.is_valid():
            employee = form.cleaned_data['employee']
            promotion = form.save(commit=False)
            
            # Set previous values
            promotion.previous_job_title = employee.job_title
            promotion.previous_department = employee.department
            promotion.previous_salary = employee.salary
            promotion.approved_by = request.user
            promotion.save()
            
            # Update employee record
            employee.job_title = promotion.new_job_title
            employee.department = promotion.new_department
            employee.salary = promotion.new_salary
            employee.save()
            
            messages.success(request, f'{employee.full_name} has been promoted successfully!')
            return redirect('promotion_list')
    else:
        form = PromotionForm()
    
    return render(request, 'employees/promotion_form.html', {'form': form})

def get_job_titles_by_department(request, department_id):
    job_titles = JobTitle.objects.filter(department_id=department_id).values('id', 'title', 'base_salary')
    return JsonResponse(list(job_titles), safe=False)
