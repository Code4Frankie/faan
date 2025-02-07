from django.shortcuts import render, redirect
from django.contrib import messages
from admin_area.models import Department, HOD

def edit_department(request, department_id):
    if 'super_admin_id' in request.session:
        try:
            department = Department.objects.get(id=department_id)
            if request.method == 'POST':
                department_name = request.POST.get('title')
                department.name = department_name
                department.save()
                messages.success(request, 'Department updated successfully.')
                return redirect('edit_departments')
            return render(request, 'admin_edit_department.html', {'department': department})
        except Department.DoesNotExist:
            messages.error(request, 'Department does not exist.')
            return redirect('edit_departments')
    else:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('login')

def delete_department(request):
    if 'super_admin_id' in request.session:
        if request.method == 'GET':
            department_id = request.GET.get('id')
            try:
                department = Department.objects.get(id=department_id)
                department.delete()
                messages.success(request, 'Department deleted successfully.')
                return redirect('edit_departments')
            except Department.DoesNotExist:
                messages.error(request, 'Department does not exist.')
                return redirect('edit_departments')
    else:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('login')
