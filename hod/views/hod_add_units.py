from django.shortcuts import render, redirect
from django.contrib import messages
from ..models import Unit, Terminal, User
from admin_area.models import HOD

def add_units(request):
    if 'hod_id' in request.session:
        hod_id = request.session['hod_id']
        hod = HOD.objects.get(id=hod_id)

        if request.method == 'POST':
            unit_name = request.POST.get('unit_name')
            terminal_id = request.POST.get('terminal_id')
            unit_head_id = request.POST.get('unit_head') 
            
            # Check if the terminal exists and belongs to the HOD's department
            try:
                terminal = Terminal.objects.get(id=terminal_id, department=hod.department)
            except Terminal.DoesNotExist:
                messages.error(request, 'Selected terminal does not exist or does not belong to your department.')
                return redirect('add_units')
            
            # Create the unit
            unit = Unit.objects.create(name=unit_name, terminal=terminal, unit_head_id=unit_head_id)
            
            # Set unit head flag for the selected user
            unit_head = User.objects.get(id=unit_head_id)
            unit_head.unit_head = True
            unit_head.save()

            messages.success(request, 'Unit created successfully.')
            return redirect('add_units')
        else:
            # Fetch the list of terminals in the HOD's department
            terminals = Terminal.objects.filter(department=hod.department)
            
            # Fetch the list of users in the department
            department_users = User.objects.filter(department=hod.department)
            
            return render(request, 'hod_add_units.html', {'terminals': terminals, 'department_users': department_users})
    else:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('login')
