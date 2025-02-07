from django.shortcuts import render, redirect
from ..models import LoggedJob

def view_logs(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user_logged_jobs = LoggedJob.objects.filter(user_id=user_id)
        context = {'user_logged_jobs': user_logged_jobs}
        return render(request, 'view_logs.html', context)
    else:
        return redirect('login')
