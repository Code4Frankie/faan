from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from admin_area.models import SuperAdmin, HOD
from hod.models import User
from admin_area.models import Department
from django.contrib.auth.hashers import make_password

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Check if the user is a super admin
        try:
            super_admin = SuperAdmin.objects.get(email=email)
            if check_password(password, super_admin.password):
                request.session['super_admin_id'] = super_admin.id
                messages.success(request, 'Welcome Admin. Your login was successful')
                return redirect('admin_dashboard')
        except SuperAdmin.DoesNotExist:
            pass
        
        # Check if the user is an HOD
        try:
            hod = HOD.objects.get(email=email)
            if check_password(password, hod.password):
                if not hod.password_changed:
                    # Redirect to profile page to change password
                    request.session['hod_id'] = hod.id
                    messages.success(request, 'Welcome, please change your password.')
                    return redirect('hod_profile')
                else:
                    # Password already changed, log in directly
                    request.session['hod_id'] = hod.id
                    messages.success(request, 'Welcome back!')
                    return redirect('hod_dashboard')
        except HOD.DoesNotExist:
            pass

        # Check if the user is a regular user in any department
        try:
            user = User.objects.get(email=email)
            print("Stored password:", user.password)
            print("Entered password (hashed):", make_password(password))

            if check_password(password, user.password):
                if not user.password_changed:
                    # Redirect to profile page to change password
                    request.session['user_id'] = user.id
                    messages.success(request, 'Welcome, please change your password.')
                    return redirect('profile')
                else:
                    # Password already changed, log in directly
                    request.session['user_id'] = user.id
                    messages.success(request, 'Welcome back!')
                    return redirect('dashboard')
        except User.DoesNotExist:
            pass

        messages.error(request, 'Invalid email or password')
    return render(request, 'login.html')
