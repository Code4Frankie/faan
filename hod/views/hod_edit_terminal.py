from django.shortcuts import render, redirect
from django.contrib import messages
from ..models import Terminal, User

def edit_terminal(request, terminal_id):
    if 'hod_id' in request.session:
        try:
            terminal = Terminal.objects.get(id=terminal_id)
            if request.method == 'POST':
                # Handle form submission to update terminal details
                terminal_name = request.POST.get('title')
                new_terminal_head_id = request.POST.get('terminal_head')
                
                # Check if the terminal head has been changed
                if terminal.terminal_head_id != new_terminal_head_id:
                    # Update the previous terminal head status to False
                    previous_terminal_head = terminal.terminal_head
                    if previous_terminal_head:
                        previous_terminal_head.terminal_head = False
                        previous_terminal_head.save()
                    
                    # Update the new terminal head status to True
                    new_terminal_head = User.objects.get(id=new_terminal_head_id)
                    new_terminal_head.terminal_head = True
                    new_terminal_head.save()
                    
                    # Update terminal details
                    terminal.name = terminal_name
                    terminal.terminal_head = new_terminal_head
                    terminal.save()
                    
                    messages.success(request, 'Terminal updated successfully.')
                    return redirect('edit_terminals')
                
                # If terminal head has not changed, update terminal name only
                terminal.name = terminal_name
                terminal.save()
                messages.success(request, 'Terminal updated successfully.')
                return redirect('edit_terminals')
                
            # Fetch the list of users in the department
            department_users = User.objects.filter(department=terminal.department)
                
            return render(request, 'hod_edit_terminal.html', {'terminal': terminal, 'department_users': department_users})
        except Terminal.DoesNotExist:
            messages.error(request, 'Terminal does not exist.')
            return redirect('edit_terminals')
    else:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('login')
