# Generated by Django 4.0.4 on 2022-08-18 18:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Edu_Master', '0061_alter_contact_us_contact_last_updated_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact_us',
            name='Contact_Last_Updated_By',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Edu_Master.admin_profile'),
        ),
    ]