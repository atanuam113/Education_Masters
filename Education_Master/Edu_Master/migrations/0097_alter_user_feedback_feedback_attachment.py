# Generated by Django 4.0.4 on 2023-07-19 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Edu_Master', '0096_user_feedback'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_feedback',
            name='Feedback_attachment',
            field=models.FileField(blank=True, null=True, upload_to='Edu_Master\\Feedback'),
        ),
    ]