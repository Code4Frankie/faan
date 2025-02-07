from django.shortcuts import render, redirect
from django.contrib import messages

def admin_verify_code(request):
    if request.method == 'POST':
        entered_code = request.POST.get('code')
        correct_code = request.session.get('verification_code')
        if entered_code == correct_code:
            return redirect('admin_reset_password')
        else:
            messages.error(request, 'Invalid verification code')
            return redirect('verify_verification_code')
    else:
        return render(request, 'admin_verify_code.html')
