# Generated by Django 4.0.4 on 2023-02-14 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Edu_Master', '0091_blog_blog_review_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='Blog_Status',
            field=models.CharField(choices=[('Active', 'Active'), ('De-active', 'De-active'), ('Hold', 'Hold'), ('Pending', 'Pending')], default='None', max_length=50),
        ),
    ]
