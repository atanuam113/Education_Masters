# Generated by Django 4.0.4 on 2022-05-29 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Edu_Master', '0039_user_user_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_DOB',
            field=models.DateField(null=True),
        ),
    ]
