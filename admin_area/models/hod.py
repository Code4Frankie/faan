from django.db import models
from .department import Department
from django.contrib.auth.hashers import make_password, check_password

class HOD(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='hod_department')
    password_changed = models.BooleanField(default=False)



    
    def save(self, *args, **kwargs):
    # Hash the password before saving, only if it's not hashed
        if not check_password(self.password, make_password(self.password)):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)


