# Generated by Django 5.0 on 2024-06-02 16:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hospital_mngmnt', '0003_patient_medicalrecord'),
    ]

    operations = [
        migrations.AddField(
            model_name='prescription',
            name='doctor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Hospital_mngmnt.doctor'),
        ),
        migrations.AddField(
            model_name='prescription',
            name='patient_name',
            field=models.CharField(default='', max_length=100),
        ),
    ]
