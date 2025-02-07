from django.shortcuts import render, redirect, get_object_or_404
from hod.models import User, Terminal, Unit
from ..models import LoggedJob
from django.contrib import messages

def edit_job(request, job_id):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
        job = get_object_or_404(LoggedJob, id=job_id)

        if job.status == 'Pending':  # Only allow editing for pending jobs
            if request.method == 'POST':
                terminal_id = request.POST.get('terminal')
                unit_id = request.POST.get('unit')
                date = request.POST.get('date')
                location = request.POST.get('location')
                equipment = request.POST.get('equipment')
                fault = request.POST.get('fault')
                rectification = request.POST.get('rectification')
                status = request.POST.get('status')

                terminal = Terminal.objects.get(id=terminal_id)
                unit = Unit.objects.get(id=unit_id)

                # Update the logged job
                job.terminal = terminal
                job.unit = unit
                job.date = date
                job.location = location
                job.equipment = equipment
                job.fault = fault
                job.rectification = rectification
                job.status = status
                job.save()

                messages.success(request, 'Job has been updated successfully.')
                return redirect('dashboard')  # Redirect to dashboard after job update

            else:
                terminals = Terminal.objects.filter(department=user.department)
                units = Unit.objects.filter(terminal__department=user.department)
                context = {
                    'job': job,
                    'terminals': terminals,
                    'units': units
                }
                return render(request, 'edit_job.html', context)
        else:
            messages.error(request, 'Only pending jobs can be edited.')
            return redirect('view_logs')  
    else:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('login')
