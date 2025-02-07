from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from admin_area.models import SuperAdmin
from django.conf import settings


def admin_forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            super_admin = SuperAdmin.objects.get(email=email)
        except SuperAdmin.DoesNotExist:
            messages.error(request, 'Invalid email address')
            return redirect('admin_forgot_password')
        
        # Generate a 6-digit verification code
        verification_code = get_random_string(length=6, allowed_chars='0123456789')

        # Send verification code to admin's email
        send_mail(
            'Password Reset Verification Code',
            f'Your verification code is: {verification_code}',
            settings.EMAIL_HOST_USER,  # Use the EMAIL_HOST_USER setting
            [email],
            fail_silently=False,
        )

        # Store verification code in session
        request.session['verification_code'] = verification_code
        request.session['admin_email'] = email

        return redirect('verify_verification_code')
    else:
        return render(request, 'admin_forgot_password.html')


