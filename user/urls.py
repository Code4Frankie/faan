from django.urls import path, include
from .views import login, dashboard, profile, add_unit, log_job, get_units, view_logs, edit_job, logout, terminal_report, unit_report, terminal_edit_units, terminal_edit_unit, terminal_delete_unit, unit_head_unit_report, download_terminal_report, download_unit_head_report

urlpatterns = [
    path('', login, name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('profile/', profile, name='profile'),
    path('add_unit/', add_unit, name='add_unit'),
    path('log_job/', log_job, name='log_job'),
    path('get_units/', get_units, name='get_units'),
    path('view_logs/', view_logs, name='view_logs'),
    path('edit_job/<int:job_id>/', edit_job, name='edit_job'),
    path('terminal_report', terminal_report, name='terminal_report'),
    path('terminal/download_unit_report/<int:unit_id>/', download_terminal_report, name='download_terminal_report'),
    path('logout/', logout, name='logout'),
    path('unit_report/', unit_report, name='unit_report'),
    path('terminal_edit_units/', terminal_edit_units, name='terminal_edit_units'),
    path('terminal_edit_unit/<int:unit_id>/', terminal_edit_unit, name='terminal_edit_unit'),
    path('terminal_delete_unit/', terminal_delete_unit, name='terminal_delete_unit'),
    path('unit_head_unit_report/', unit_head_unit_report, name='unit_head_unit_report'),
    path('unit_head/download_unit_report/', download_unit_head_report, name='download_unit_head_report'),



]

