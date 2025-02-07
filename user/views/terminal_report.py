from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from hod.models import User, Terminal, Unit
from django.http import HttpResponse
from openpyxl import Workbook

def terminal_report(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)

        # Ensure the user is a terminal head
        terminal = Terminal.objects.filter(terminal_head=user).first()
        if terminal:
            units = Unit.objects.filter(terminal=terminal)
            context = {
                'terminal_name': terminal.name,
                'units': units
            }
            return render(request, 'terminal_report.html', context)
        else:
            messages.error(request, 'You are not assigned to any terminal.')

    else:
        messages.error(request, 'Please log in to access')
        return redirect('login')



def download_terminal_report(request, unit_id):
    # Retrieve the unit object
    unit = get_object_or_404(Unit, id=unit_id)
    
    # Create a new workbook
    wb = Workbook()
    ws = wb.active

    # Define headers
    headers = [
        'Terminal Name', 'Unit Name', 'User Name', 'Email', 
        'Date of fault', 'Place of fault', 'Equipment', 'Fault', 
        'Rectification', 'Status'
    ]
    ws.append(headers)

    # Add data to the worksheet
    for report in unit.loggedjob_set.all():
        # Convert datetime to naive datetime (without timezone information)
        date_added = report.date.replace(tzinfo=None) if report.date else None
        
        ws.append([
            report.terminal.name,
            unit.name,
            f"{report.user.first_name} {report.user.last_name}",
            report.user.email,
            date_added,
            report.location,
            report.equipment,
            report.fault,
            report.rectification,
            report.status
        ])
    
    # Protect the worksheet
    ws.protection.sheet = True
    ws.protection.password = 'password'  # Set a password for the protection, can be any string

    # Save the workbook
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename={unit.name}_report.xlsx'
    wb.save(response)
    return response
