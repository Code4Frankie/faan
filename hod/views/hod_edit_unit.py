from django.shortcuts import render, redirect
from django.contrib import messages
from ..models import Unit, Terminal, User

def edit_unit(request, unit_id):
    if 'hod_id' in request.session:
        try:
            unit = Unit.objects.get(id=unit_id)
            if request.method == 'POST':
                # Handle form submission to update unit details
                unit_name = request.POST.get('unit_name')
                new_terminal_id = request.POST.get('terminal_id')
                new_unit_head_id = request.POST.get('unit_head')
                
                # Check if the terminal has been changed
                if unit.terminal_id != new_terminal_id:
                    # Update the terminal
                    new_terminal = Terminal.objects.get(id=new_terminal_id)
                    unit.terminal = new_terminal
                
                # Check if the unit head has been changed
                if unit.unit_head_id != new_unit_head_id:
                    # Update the previous unit head status to False
                    previous_unit_head = unit.unit_head
                    if previous_unit_head:
                        previous_unit_head.unit_head = False
                        previous_unit_head.save()
                    
                    # Update the new unit head status to True
                    new_unit_head = User.objects.get(id=new_unit_head_id)
                    new_unit_head.unit_head = True
                    new_unit_head.save()
                    
                    # Update unit details
                    unit.name = unit_name
                    unit.unit_head = new_unit_head
                    unit.save()
                    
                    messages.success(request, 'Unit updated successfully.')
                    return redirect('edit_units')
                
                # If terminal head has not changed, update unit name only
                unit.name = unit_name
                unit.save()
                messages.success(request, 'Unit updated successfully.')
                return redirect('edit_units')
                
            # Fetch the list of terminals and users in the department
            terminals = Terminal.objects.all()
            department_users = User.objects.filter(department=unit.terminal.department)
                
            return render(request, 'hod_edit_unit.html', {'unit': unit, 'terminals': terminals, 'department_users': department_users})
        except Unit.DoesNotExist:
            messages.error(request, 'Unit does not exist.')
            return redirect('edit_units')
    else:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('login')
