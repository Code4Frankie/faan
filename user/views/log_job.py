# views.py

from django.shortcuts import render, redirect
from hod.models import User, Terminal, Unit
from ..models import LoggedJob
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone

def log_job(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)

        if request.method == 'POST':
            terminal_id = request.POST.get('terminal')
            unit_id = request.POST.get('unit')
            date_str = request.POST.get('date')  # Assuming the date is in ISO format
            location = request.POST.get('location')
            equipment = request.POST.get('equipment')
            fault = request.POST.get('fault')
            rectification = request.POST.get('rectification')
            status = request.POST.get('status')

            terminal = Terminal.objects.get(id=terminal_id)
            unit = Unit.objects.get(id=unit_id)

            # Convert the string date to a datetime object
            date = timezone.make_aware(timezone.datetime.fromisoformat(date_str))

            # Create the logged job
            logged_job = LoggedJob.objects.create(
                user=user,
                terminal=terminal,
                unit=unit,
                date=date,
                location=location,
                equipment=equipment,
                fault=fault,
                rectification=rectification,
                status=status
            )
            messages.success(request, 'Job has been Logged Successfully.')
            return redirect('dashboard')  # Redirect to dashboard after job submission

        else:
            terminals = Terminal.objects.filter(department=user.department)
            units = Unit.objects.filter(terminal__department=user.department)
            context = {
                'terminals': terminals,
                'units': units
            }
            return render(request, 'log_job.html', context)
    else:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('login')




def get_units(request):
    terminal_id = request.GET.get('terminal_id')
    units = Unit.objects.filter(terminal_id=terminal_id).values('id', 'name')
    return JsonResponse(list(units), safe=False)
