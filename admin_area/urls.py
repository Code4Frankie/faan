
from django.urls import path, include
from .views import admin_dashboard, edit_departments, admin_logout, admin_profile, admin_verify_code, admin_forgot_password, admin_reset_password, add_department, add_hod, view_hods, edit_department, delete_department, delete_hod

urlpatterns = [
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin/logout/', admin_logout, name='admin_logout'),
    path('admin_profile/', admin_profile, name='admin_profile'),
    path('admin/forgot-password/', admin_forgot_password, name='admin_forgot_password'),
    path('admin/verify-code/', admin_verify_code, name='admin_verify_code'),
    path('admin/reset-password/', admin_reset_password, name='admin_reset_password'),
    path('add_department/', add_department, name='add_department'),
    path('add_hod/', add_hod, name='add_hod'),
    path('edit_departments/', edit_departments, name='edit_departments'),
    path('view_hods', view_hods, name='view_hods'),
    path('edit_department/<int:department_id>/', edit_department, name='edit_department'),
    path('delete_department/', delete_department, name='delete_department'),
    path('delete_hod/<int:hod_id>/', delete_hod, name='delete_hod'),






]
