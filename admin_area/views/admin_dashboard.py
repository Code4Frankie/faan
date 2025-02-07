from django.shortcuts import render, redirect
from django.contrib import messages
from ..models import Department, HOD
from hod.models import Terminal, Unit, User

def admin_dashboard(request):
    # Check if super_admin_id is present in session
    if 'super_admin_id' in request.session:
        # Fetch counts from the database
        total_departments = Department.objects.count()
        total_terminals = Terminal.objects.count()
        total_units = Unit.objects.count()
        total_hods = HOD.objects.count()
        total_users = User.objects.count()

        # Calculate total users
        total_users_count = total_hods + total_users + 1  # +1 for the super admin

        # Fetch departments and related data
        departments = Department.objects.all()
        for department in departments:
            department.hod = HOD.objects.filter(department=department).first()
            department.num_units = Unit.objects.filter(terminal__department=department).count()
            department.num_terminals = Terminal.objects.filter(department=department).count()

        context = {
            'total_departments': total_departments,
            'total_terminals': total_terminals,
            'total_units': total_units,
            'total_users': total_users_count,
            'departments': departments
        }

        # Render admin dashboard with context data
        return render(request, 'admin_dashboard.html', context)
    else:
        # Redirect to login page or any other page
        messages.info(request, 'Please log in to access the admin page')
        return redirect('login')

def admin_logout(request):
    # Remove super_admin_id from session
    if 'super_admin_id' in request.session:
        del request.session['super_admin_id']
        messages.success(request, 'Admin, You have been logged out')

    return redirect('login')
