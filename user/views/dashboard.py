from django.shortcuts import render, redirect
from hod.models import User, Terminal, Unit
from ..models import LoggedJob


def dashboard(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
        department_name = user.department.name
        
        # Get total number of terminals in the user's department
        total_terminals = Terminal.objects.filter(department=user.department).count()
        
        # Get total number of units across all terminals in the user's department
        total_units = Unit.objects.filter(terminal__department=user.department).count()
        
        # Get the terminal where the user is the terminal head
        terminal = Terminal.objects.filter(terminal_head=user).first()
        
        # Get the total number of units in the terminal where the user is the terminal head
        terminal_units_count = Unit.objects.filter(terminal=terminal).count() if terminal else 0

        # Get the total number of jobs logged by the current user

        num_jobs_logged = LoggedJob.objects.filter(user=user).count()

        
        context = {
            'user': user,
            'department_name': department_name,
            'total_terminals': total_terminals,
            'total_units': total_units,
            'terminal': terminal,
            'terminal_units_count': terminal_units_count,
            'num_jobs_logged': num_jobs_logged

        }
        
        return render(request, 'dashboard.html', context)
    else:
        # Handle case where user is not logged in
        return redirect('login')



def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect('login')
