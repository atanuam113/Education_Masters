# Generated by Django 3.2.4 on 2022-03-17 06:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Edu_Master', '0012_alter_events_event_end_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='events',
            name='Event_End_Time',
        ),
    ]