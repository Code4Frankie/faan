from django.db import models
from admin_area.models import Department
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    terminal_head = models.BooleanField(default=False)
    unit_head = models.BooleanField(default=False)
    password_changed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        # Hash the password before saving, only if it's not hashed
        if not check_password(self.password, make_password(self.password)):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)


