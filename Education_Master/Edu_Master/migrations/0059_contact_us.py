# Generated by Django 4.0.4 on 2022-08-14 21:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Edu_Master', '0058_delete_contact_us'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact_us',
            fields=[
                ('Contact_ID', models.AutoField(primary_key=True, serialize=False)),
                ('Contact_Name', models.CharField(default='None', max_length=200)),
                ('Contact_Email', models.EmailField(max_length=254)),
                ('Contact_Message', models.TextField(default='None')),
                ('Contact_Created_By', models.CharField(default='None', max_length=200)),
                ('Contact_Created_Date', models.DateTimeField(null=True)),
                ('Contact_Last_Updated_Date', models.DateTimeField(null=True)),
                ('Contact_Effective_End_Date', models.DateTimeField(null=True)),
                ('Contact_Version', models.CharField(default='1', max_length=20)),
                ('Contact_Status', models.CharField(choices=[('Solved', 'Solved'), ('Pending', 'Pending'), ('Hold', 'Hold')], default='None', max_length=100)),
                ('Contact_Last_Updated_By', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Edu_Master.admin_profile')),
            ],
        ),
    ]