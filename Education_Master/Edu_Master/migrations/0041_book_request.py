# Generated by Django 4.0.4 on 2022-06-18 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Edu_Master', '0040_alter_user_user_dob'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book_Request',
            fields=[
                ('Book_Request_ID', models.AutoField(primary_key=True, serialize=False)),
                ('Book_Request_Name', models.CharField(default='None', max_length=500)),
                ('Book_Request_Author', models.CharField(default='None', max_length=200)),
                ('Book_Request_ISBN', models.CharField(default='0', max_length=30)),
                ('Book_Request_Date', models.DateTimeField()),
            ],
        ),
    ]
