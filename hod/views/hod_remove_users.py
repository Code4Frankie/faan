from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from admin_area.models import HOD
from ..models import User

def hod_remove_users(request):
    # Check if hod_id is in session
    if 'hod_id' in request.session:
        hod_id = request.session['hod_id']
        hod = HOD.objects.get(id=hod_id)

        # Fetch all regular users belonging to the HOD's department
        users = User.objects.filter(department=hod.department)

        if request.method == 'POST':
            # Get the user ID from the form data
            user_id = request.POST.get('user_id')
            # Retrieve the user object
            user = get_object_or_404(User, id=user_id)

            # Delete the user
            user.delete()
            messages.success(request, 'User deleted successfully.')
            return redirect('hod_remove_users')

        return render(request, 'hod_remove_users.html', {'hod': hod, 'users': users})
    else:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('login')
