# Generated by Django 4.0.4 on 2022-08-31 17:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Edu_Master', '0062_alter_contact_us_contact_last_updated_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher_Profile_Log',
            fields=[
                ('TPLog_PK', models.AutoField(primary_key=True, serialize=False)),
                ('TPLog_Name', models.CharField(default='', max_length=200)),
                ('TPLog_Email', models.CharField(default='', max_length=200)),
                ('TPLog_Phone', models.CharField(default='None', max_length=200)),
                ('TPLog_DOB', models.DateField()),
                ('TPLog_Address', models.CharField(default='None', max_length=500)),
                ('TPLog_Dept', models.CharField(default='None', max_length=500)),
                ('TPLog_Status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive'), ('Hold', 'Hold')], default='', max_length=20)),
                ('TPLog_Bio', models.CharField(default='None', max_length=1000)),
                ('TPLog_Profile_Pic', models.ImageField(blank=True, null=True, upload_to='Edu_Master\\Teacher')),
                ('TPLog_Github', models.CharField(default='None', max_length=200)),
                ('TPLog_Linkedin', models.CharField(default='None', max_length=200)),
                ('TPLog_Twitter', models.CharField(default='None', max_length=200)),
                ('TPLog_Updated_Date', models.DateTimeField(blank=True, null=True)),
                ('TPLog_Effective_End_Date', models.DateTimeField(blank=True, null=True)),
                ('TPLog_Teacher_PK', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Edu_Master.teacher_profile')),
                ('TPLog_Updated_By', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Student_Profile_Log',
            fields=[
                ('SPLog_PK', models.AutoField(primary_key=True, serialize=False)),
                ('SPLOG_Name', models.CharField(default='', max_length=200)),
                ('SPLOG_Email', models.CharField(default='', max_length=200)),
                ('SPLOG_Phone', models.CharField(default='None', max_length=200)),
                ('SPLOG_DOB', models.DateField()),
                ('SPLOG_Address', models.CharField(default='None', max_length=500)),
                ('SPLOG_Status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive'), ('Hold', 'Hold')], default='', max_length=20)),
                ('SPLOG_Bio', models.CharField(default='None', max_length=1000)),
                ('SPLOG_Profile_Pic', models.ImageField(blank=True, null=True, upload_to='Edu_Master\\Student')),
                ('SPLOG_Github', models.CharField(default='None', max_length=200)),
                ('SPLOG_Linkedin', models.CharField(default='None', max_length=200)),
                ('SPLOG_Twitter', models.CharField(default='None', max_length=200)),
                ('SPLOG_Updated_Date', models.DateTimeField(blank=True, null=True)),
                ('SPLOG_Effective_End_Date', models.DateTimeField(blank=True, null=True)),
                ('SPLOG_Student_PK', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Edu_Master.student_profile')),
                ('SPLog_Updated_By', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Librarian_Profile_Log',
            fields=[
                ('LPLog_PK', models.AutoField(primary_key=True, serialize=False)),
                ('LPLog_Name', models.CharField(default='', max_length=200)),
                ('LPLog_Email', models.CharField(default='', max_length=200)),
                ('LPLog_Phone', models.CharField(default='None', max_length=200)),
                ('LPLog_DOB', models.DateField()),
                ('LPLog_Address', models.CharField(default='None', max_length=500)),
                ('LPLog_Dept', models.CharField(default='None', max_length=500)),
                ('LPLog_Status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive'), ('Hold', 'Hold')], default='', max_length=20)),
                ('LPLog_Bio', models.CharField(default='None', max_length=1000)),
                ('LPLog_Profile_Pic', models.ImageField(blank=True, null=True, upload_to='Edu_Master\\Librarian')),
                ('LPLog_Github', models.CharField(default='None', max_length=200)),
                ('LPLog_Linkedin', models.CharField(default='None', max_length=200)),
                ('LPLog_Twitter', models.CharField(default='None', max_length=200)),
                ('LPLog_Updated_Date', models.DateTimeField(blank=True, null=True)),
                ('LPLog_Effective_End_Date', models.DateTimeField(blank=True, null=True)),
                ('LPLog_Admin_PK', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Edu_Master.librarian_profile')),
                ('LPLog_Updated_By', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Admin_Profile_Log',
            fields=[
                ('APLog_PK', models.AutoField(primary_key=True, serialize=False)),
                ('APLog_Name', models.CharField(default='', max_length=200)),
                ('APLog_Email', models.CharField(default='', max_length=200)),
                ('APLog_Phone', models.CharField(default='None', max_length=200)),
                ('APLog_DOB', models.DateField()),
                ('APLog_Address', models.CharField(default='None', max_length=500)),
                ('APLog_Dept', models.CharField(default='None', max_length=500)),
                ('APLog_Status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive'), ('Hold', 'Hold')], default='', max_length=20)),
                ('APLog_Bio', models.CharField(default='None', max_length=1000)),
                ('APLog_Profile_Pic', models.ImageField(blank=True, null=True, upload_to='Edu_Master\\Admin')),
                ('APLog_Github', models.CharField(default='None', max_length=200)),
                ('APLog_Linkedin', models.CharField(default='None', max_length=200)),
                ('APLog_Twitter', models.CharField(default='None', max_length=200)),
                ('APLog_Updated_Date', models.DateTimeField(blank=True, null=True)),
                ('APLog_Effective_End_Date', models.DateTimeField(blank=True, null=True)),
                ('APLog_Admin_PK', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Edu_Master.admin_profile')),
                ('APLog_Updated_By', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]