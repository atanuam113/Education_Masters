# Generated by Django 4.0.4 on 2022-05-02 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Edu_Master', '0027_alter_books_book_cover_alter_books_book_pdf_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='student_library_profile',
            name='Student_Status',
            field=models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive'), ('Hold', 'Hold')], default='', max_length=20),
        ),
    ]