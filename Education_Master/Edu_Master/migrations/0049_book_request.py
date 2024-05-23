# Generated by Django 4.0.4 on 2022-06-21 20:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Edu_Master', '0048_delete_book_request'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book_Request',
            fields=[
                ('Book_Request_ID', models.AutoField(primary_key=True, serialize=False)),
                ('Book_Request_Name', models.CharField(default='None', max_length=500)),
                ('Book_Request_Author', models.CharField(default='None', max_length=200)),
                ('Book_Request_ISBN', models.CharField(default='0', max_length=30)),
                ('Book_Request_Date', models.DateTimeField(auto_now=True)),
                ('Book_Request_By', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Edu_Master.student_profile')),
            ],
        ),
    ]