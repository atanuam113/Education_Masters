# Generated by Django 4.0.4 on 2022-09-21 18:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Edu_Master', '0076_address_book_ab_party_email_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Email_Detail',
            fields=[
                ('Email_Id', models.AutoField(primary_key=True, serialize=False)),
                ('Email_Sender', models.CharField(default='None', max_length=200)),
                ('Email_Receiver', models.CharField(default='None', max_length=200)),
                ('Email_Receiver_Name', models.CharField(default='None', max_length=200)),
                ('Email_subject', models.CharField(default='None', max_length=150)),
                ('Email_Message', models.TextField(default='')),
                ('Email_DateTime', models.DateTimeField(blank=True, null=True)),
                ('Email_Last_Update_Date', models.DateTimeField(blank=True, null=True)),
                ('Email_Effective_End_Date', models.DateTimeField(blank=True, null=True)),
                ('Email_Last_Updated_By', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Edu_Master.admin_profile')),
            ],
        ),
    ]