# Generated by Django 4.0.4 on 2022-06-20 19:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Edu_Master', '0042_alter_book_request_book_request_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='book_request',
            name='Book_Request_By',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]