# Generated by Django 4.0.4 on 2022-09-22 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Edu_Master', '0078_alter_email_detail_email_last_updated_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='email_detail',
            name='Email_Attachment',
            field=models.FileField(blank=True, null=True, upload_to='Edu_Master\\Email'),
        ),
        migrations.AddField(
            model_name='email_detail',
            name='Email_BCC',
            field=models.CharField(default='None', max_length=300),
        ),
        migrations.AddField(
            model_name='email_detail',
            name='Email_CC',
            field=models.CharField(default='None', max_length=300),
        ),
    ]