
from django.urls import path, include

urlpatterns = [
    path('', include('user.urls')),
    path('admin/', include('admin_area.urls')),
    path('hod/', include('hod.urls')),  

]
