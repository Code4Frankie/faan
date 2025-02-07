# terminal_head_add_units.py
from django.shortcuts import render, redirect
from django.contrib import messages
from hod.models import Unit, Terminal, User

def add_unit(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)

        if user.terminal_head:  # Check if the user is a terminal head
            if request.method == 'POST':
                unit_name = request.POST.get('unit_name')
                # Get the terminal where the user is the terminal head
                terminal = Terminal.objects.filter(terminal_head=user).first()
        
                unit_head_id = request.POST.get('unit_head')
                
                # Create the unit
                unit = Unit.objects.create(name=unit_name, terminal=terminal, unit_head_id=unit_head_id)
                
                # Set unit head flag for the selected user
                unit_head = User.objects.get(id=unit_head_id)
                unit_head.unit_head = True
                unit_head.save()

                messages.success(request, 'Unit created successfully.')
                return redirect('dashboard')  # Adjust redirect as needed
            else:
                # Fetch the list of users in the terminal
                department_users = User.objects.filter(department=user.department)

                return render(request, 'add_unit.html', {'department_users': department_users})
        else:
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('login')
    else:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('login')
