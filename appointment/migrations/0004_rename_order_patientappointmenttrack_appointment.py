# Generated by Django 3.2.9 on 2022-05-30 06:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0003_alter_takeappointment_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='patientappointmenttrack',
            old_name='order',
            new_name='appointment',
        ),
    ]
