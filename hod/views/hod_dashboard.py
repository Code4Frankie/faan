from django.shortcuts import render, redirect
from django.contrib import messages
from admin_area.models import HOD
from ..models import Terminal, Unit, User
from django.shortcuts import render, redirect
from django.contrib import messages

def hod_dashboard(request):
    if 'hod_id' in request.session:
        hod_id = request.session['hod_id']
        hod = HOD.objects.get(id=hod_id)
        
        # Fetch terminals associated with the HOD's department
        terminals = Terminal.objects.filter(department=hod.department)
        
        # Total number of terminals
        total_terminals = terminals.count()
        
        # Total number of units across all terminals
        total_units = Unit.objects.filter(terminal__in=terminals).count()
        
        # Total number of users in the department
        total_users = User.objects.filter(department=hod.department).count()
        
        # Calculate number of units in each terminal
        for terminal in terminals:
            terminal.num_units = Unit.objects.filter(terminal=terminal).count()
        
        context = {
            'hod': hod,
            'terminals': terminals,
            'total_terminals': total_terminals,
            'total_units': total_units,
            'total_users': total_users,
        
        }
    else:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('login')
    
    return render(request, 'hod_dashboard.html', context)







def hod_logout(request):
    # Check if hod_id is in session
    if 'hod_id' in request.session:
        # Clear hod_id from session
        del request.session['hod_id']
        messages.success(request, 'You have been logged out successfully.')
    
    # Redirect to login page
    return redirect('login')
