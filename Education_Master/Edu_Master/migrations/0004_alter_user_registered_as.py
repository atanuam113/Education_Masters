# Generated by Django 3.2.4 on 2022-03-13 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Edu_Master', '0003_auto_20220313_2033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='Registered_As',
            field=models.CharField(choices=[('None', 'None'), ('Student', 'Student'), ('Teacher', 'Teacher'), ('Admin', 'Admin')], default='', max_length=20),
        ),
    ]