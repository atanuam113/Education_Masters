# Generated by Django 4.0.4 on 2023-01-17 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Edu_Master', '0090_blog_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='Blog_Review_status',
            field=models.CharField(choices=[('Enable', 'Enable'), ('Disable', 'Disable'), ('Hold', 'Hold')], default='Enable', max_length=50),
        ),
    ]