# Generated by Django 4.0.4 on 2022-07-08 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Edu_Master', '0051_book_request_book_request_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher_profile',
            name='Teacher_Dept',
            field=models.CharField(default='None', max_length=500),
        ),
    ]
