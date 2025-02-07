from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from admin_area.models import HOD
from ..models import Terminal

def edit_terminals(request):
    if 'hod_id' in request.session:
        hod_id = request.session['hod_id']
        hod = get_object_or_404(HOD, id=hod_id)

        # Fetch terminals associated with the HOD's department
        terminals = Terminal.objects.filter(department=hod.department)
        return render(request, 'hod_edit_terminals.html', {'terminals': terminals})
    else:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('login')

def delete_terminal(request):
    if 'hod_id' in request.session:
        hod_id = request.session['hod_id']
        hod = get_object_or_404(HOD, id=hod_id)

        if request.method == 'GET':
            terminal_id = request.GET.get('id')
            try:
                terminal = Terminal.objects.get(id=terminal_id, department=hod.department)
                terminal.delete()
                messages.success(request, 'Terminal deleted successfully.')
                return redirect('edit_terminals')
            except Terminal.DoesNotExist:
                messages.error(request, 'Terminal does not exist or you do not have permission to delete it.')
                return redirect('edit_terminals')
    else:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('login')
