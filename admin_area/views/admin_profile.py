from django.shortcuts import render, redirect
from django.contrib import messages
from admin_area.models import SuperAdmin
from django.contrib.auth.hashers import make_password, check_password

def admin_profile(request):
    # Check if super_admin_id is present in session
    super_admin_id = request.session.get('super_admin_id')
    if super_admin_id:
        super_admin = SuperAdmin.objects.get(id=super_admin_id)
        if request.method == 'POST':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            # Update SuperAdmin instance with new values
            super_admin.first_name = first_name
            super_admin.last_name = last_name
            super_admin.email = email

            # Validate and update password if provided
            if password and password == confirm_password and len(password) >= 6:
                super_admin.password = make_password(password)
                super_admin.save()
                messages.success(request, 'Profile updated successfully')
            elif password != confirm_password:
                messages.error(request, 'Passwords do not match')
            elif len(password) < 6:
                messages.error(request, 'Password must be at least 6 characters long')
            else:
                super_admin.save()
                messages.success(request, 'Profile updated successfully')
        
        return render(request, 'admin_profile.html', {'super_admin': super_admin})
    else:
        # Redirect to login page or any other page
        messages.info(request, 'Please log in to access the admin page')
        return redirect('login')
