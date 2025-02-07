from django.shortcuts import render, redirect
from django.contrib import messages
from hod.models import Unit, User

def terminal_edit_unit(request, unit_id):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)

        if user.terminal_head:  # Check if the user is a terminal head
            try:
                unit = Unit.objects.get(id=unit_id, terminal__terminal_head=user)
                if request.method == 'POST':
                    unit_name = request.POST.get('unit_name')
                    new_unit_head_id = request.POST.get('unit_head')
                    
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
                    
                    # If unit head has not changed, update unit name only
                    unit.name = unit_name
                    unit.save()
                    messages.success(request, 'Unit updated successfully.')
                    return redirect('edit_units')
                    
                # Fetch the list of users in the terminal
                department_users = User.objects.filter(department=user.department)
                    
                return render(request, 'terminal_head_edit_unit.html', {'unit': unit, 'department_users': department_users})
            except Unit.DoesNotExist:
                messages.error(request, 'Unit does not exist or you do not have permission to edit it.')
                return redirect('edit_units')
        else:
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('login')
    else:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('login')
