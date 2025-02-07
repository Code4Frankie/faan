from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from admin_area.models import HOD
from ..models import Terminal, Unit

def edit_units(request):
    if 'hod_id' in request.session:
        hod_id = request.session['hod_id']
        hod = get_object_or_404(HOD, id=hod_id)

        # Fetch terminals associated with the HOD's department
        terminals = Terminal.objects.filter(department=hod.department)
        
        # Fetch units associated with the terminals in the HOD's department
        units = Unit.objects.filter(terminal__in=terminals)
        
        return render(request, 'hod_edit_units.html', {'units': units})
    else:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('login')

def delete_unit(request):
    if 'hod_id' in request.session:
        hod_id = request.session['hod_id']
        hod = get_object_or_404(HOD, id=hod_id)

        if request.method == 'GET':
            unit_id = request.GET.get('id')
            try:
                # Fetch terminals associated with the HOD's department
                terminals = Terminal.objects.filter(department=hod.department)
                
                # Try to get the unit only if it belongs to the terminals in the HOD's department
                unit = Unit.objects.get(id=unit_id, terminal__in=terminals)
                unit.delete()
                messages.success(request, 'Unit deleted successfully.')
                return redirect('edit_units')
            except Unit.DoesNotExist:
                messages.error(request, 'Unit does not exist or you do not have permission to delete it.')
                return redirect('edit_units')
    else:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('login')
