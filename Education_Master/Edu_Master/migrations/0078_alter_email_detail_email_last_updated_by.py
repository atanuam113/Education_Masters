# Generated by Django 4.0.4 on 2022-09-21 18:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Edu_Master', '0077_email_detail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email_detail',
            name='Email_Last_Updated_By',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
