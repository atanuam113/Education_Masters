# Generated by Django 4.0.4 on 2022-05-09 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Edu_Master', '0033_remove_course_detail_course_trainer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='course_detail',
            name='Course_Rating',
            field=models.CharField(choices=[('Introductory', 'Introductory'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')], default='0', max_length=20),
        ),
    ]