# Generated by Django 4.0.4 on 2022-05-02 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Edu_Master', '0028_student_library_profile_student_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='student_library_profile',
            name='Library_Password',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='student_library_profile',
            name='Library_user_ID',
            field=models.CharField(default='', max_length=100),
        ),
    ]
