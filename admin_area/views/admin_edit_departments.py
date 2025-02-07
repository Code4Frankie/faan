from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from admin_area.models import Department

def edit_departments(request):
    if 'super_admin_id' in request.session:
        departments = Department.objects.all()
        return render(request, 'admin_edit_departments.html', {'departments': departments})
    else:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('login')






def delete_department(request):
    if 'super_admin_id' in request.session:
        if request.method == 'GET' and 'id' in request.GET:
            department_id = request.GET.get('id')
            department = get_object_or_404(Department, id=department_id)
            # Delete related objects first (e.g., HOD)
            if department.hod:
                department.hod.delete()
            department.delete()
            messages.success(request, 'Department deleted successfully.')
        else:
            messages.error(request, 'Invalid request.')
        return redirect('edit_departments')
    else:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('login')