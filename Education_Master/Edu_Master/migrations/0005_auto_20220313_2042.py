# Generated by Django 3.2.4 on 2022-03-13 15:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Edu_Master', '0004_alter_user_registered_as'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_admin',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_student',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_trainer',
        ),
    ]