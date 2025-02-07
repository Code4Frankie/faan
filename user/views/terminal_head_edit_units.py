from django.shortcuts import render, redirect
from django.contrib import messages
from hod.models import Unit, Terminal, User

def terminal_edit_units(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)

        if user.terminal_head:  # Check if the user is a terminal head
            units = Unit.objects.filter(terminal__terminal_head=user)
            return render(request, 'terminal_head_edit_units.html', {'units': units})
        else:
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('login')
    else:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('login')


def terminal_delete_unit(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)

        if user.terminal_head:  # Check if the user is a terminal head
            if request.method == 'GET':
                unit_id = request.GET.get('id')
                try:
                    unit = Unit.objects.get(id=unit_id, terminal__terminal_head=user)
                    unit.delete()
                    messages.success(request, 'Unit deleted successfully.')
                    return redirect('edit_units')
                except Unit.DoesNotExist:
                    messages.error(request, 'Unit does not exist or you do not have permission to delete it.')
                    return redirect('edit_units')
        else:
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('login')
    else:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('login')
