# Generated by Django 4.0.4 on 2022-08-14 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Edu_Master', '0055_address_book'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact_us',
            name='Contact_Created_By',
            field=models.CharField(default='None', max_length=200),
        ),
        migrations.AddField(
            model_name='contact_us',
            name='Contact_Created_Date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='contact_us',
            name='Contact_Effective_End_Date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='contact_us',
            name='Contact_Last_Updated_By',
            field=models.CharField(default='None', max_length=200),
        ),
        migrations.AddField(
            model_name='contact_us',
            name='Contact_Last_Updated_Date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='contact_us',
            name='Contact_Status',
            field=models.CharField(choices=[('Solved', 'Solved'), ('Pending', 'Pending'), ('Hold', 'Hold')], default='None', max_length=100),
        ),
        migrations.AddField(
            model_name='contact_us',
            name='Contact_Version',
            field=models.CharField(default='1', max_length=20),
        ),
    ]
