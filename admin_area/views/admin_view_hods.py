from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from admin_area.models import HOD


def view_hods(request):
    if 'super_admin_id' in request.session:
        hods = HOD.objects.all()
        return render(request, 'admin_view_hods.html', {'hods': hods})
    else:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('login')




def delete_hod(request, hod_id):
    if 'super_admin_id' in request.session:
        hod = get_object_or_404(HOD, id=hod_id)
        department = hod.department
        hod.delete()
        messages.success(request, f'HOD {hod.first_name} {hod.last_name} deleted successfully.')
        # Redirect back to the view HODs page
        return redirect('view_hods')
    else:
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('login')
