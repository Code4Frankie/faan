from django.shortcuts import render, redirect
from admin_area.models import HOD
from ..models import Terminal

def view_terminal_reports(request):
    if 'hod_id' in request.session:
        hod_id = request.session['hod_id']
        hod = HOD.objects.get(id=hod_id)

        # Fetch terminals associated with the HOD's department
        terminals = Terminal.objects.filter(department=hod.department)

        context = {
            'hod': hod,
            'terminals': terminals,
        }
        return render(request, 'hod_terminal_reports.html', context)
    else:
        return redirect('login')
