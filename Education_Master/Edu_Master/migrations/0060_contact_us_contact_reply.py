# Generated by Django 4.0.4 on 2022-08-14 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Edu_Master', '0059_contact_us'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact_us',
            name='Contact_Reply',
            field=models.TextField(default='None'),
        ),
    ]
