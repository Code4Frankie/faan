# Generated by Django 5.0.4 on 2024-05-05 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_area', '0004_department_hod_department_num_terminals_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='hod',
            name='password_changed',
            field=models.BooleanField(default=False),
        ),
    ]
