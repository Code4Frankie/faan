from django.shortcuts import render, redirect
from django.contrib import messages
from admin_area.models import HOD
from ..models import User
from ..models import Terminal

def hod_add_terminal(request):
    if 'hod_id' in request.session:
        hod_id = request.session['hod_id']
        hod = HOD.objects.get(id=hod_id)

        if request.method == 'POST':
            terminal_name = request.POST.get('terminal_name')
            terminal_head_id = request.POST.get('terminal_head')

            # Get the selected terminal head user
            terminal_head = User.objects.get(id=terminal_head_id)

            # Create the terminal object
            terminal = Terminal.objects.create(
                name=terminal_name,
                department=hod.department,
                terminal_head=terminal_head
            )

            # Set terminal head flag for the selected user
            terminal_head.terminal_head = True
            terminal_head.save()

            messages.success(request, 'Terminal created successfully.')
            return redirect('hod_dashboard')

        # Get all users in the hod's department to populate the dropdown list
        department_users = User.objects.filter(department=hod.department)

        return render(request, 'hod_add_terminal.html', {'hod': hod, 'department_users': department_users})
    else:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('login')
