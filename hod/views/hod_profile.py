from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from admin_area.models import HOD

def hod_profile(request):
    # Check if hod_id is in session
    if 'hod_id' in request.session:
        hod_id = request.session['hod_id']
        hod = HOD.objects.get(id=hod_id)
        
        if request.method == 'POST':
            # Handle form submission to update profile
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            new_password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            
            # Update hod's profile
            hod.first_name = first_name
            hod.last_name = last_name
            hod.email = email
            
            # Validate and hash the new password if provided
            if new_password:
                # Check if new password and confirm password match
                if new_password == confirm_password:
                    # Hash the new password before saving
                    hashed_password = make_password(new_password)
                    hod.password = hashed_password
                    # Update password_changed to True
                    hod.password_changed = True
                else:
                    messages.error(request, 'Passwords do not match. Please try again.')
                    return render(request, 'hod_profile.html', {'hod': hod})

            hod.save()
            messages.success(request, 'Profile updated successfully.')
            # Redirect to hod_dashboard if password changed
            if hod.password_changed:
                return redirect('hod_dashboard')
        
        return render(request, 'hod_profile.html', {'hod': hod})
    else:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('login')
