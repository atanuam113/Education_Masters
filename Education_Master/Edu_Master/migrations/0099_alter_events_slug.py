# Generated by Django 4.0.4 on 2023-08-18 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Edu_Master', '0098_alter_events_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='slug',
            field=models.SlugField(default=''),
        ),
    ]