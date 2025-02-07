from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from admin_area.models import SuperAdmin

def admin_reset_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('admin_reset_password')
        
        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters long')
            return redirect('admin_reset_password')
        
        email = request.session.get('admin_email')
        try:
            super_admin = SuperAdmin.objects.get(email=email)
            super_admin.password = make_password(password)
            super_admin.save()
            messages.success(request, 'Password reset successfully')
            return redirect('login')
        except SuperAdmin.DoesNotExist:
            messages.error(request, 'Admin does not exist')
            return redirect('admin_reset_password')
    else:
        return render(request, 'admin_reset_password.html')
