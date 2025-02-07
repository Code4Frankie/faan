from django.shortcuts import render, redirect
from django.contrib import messages
from admin_area.models import HOD

def hod_edit_users(request):
    # Check if hod_id is in session
    if 'hod_id' in request.session:
        hod_id = request.session['hod_id']
        hod = HOD.objects.get(id=hod_id)

        return render(request, 'hod_edit_users.html', {'hod': hod})
    else:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('login')