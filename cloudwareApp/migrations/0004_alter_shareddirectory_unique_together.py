# Generated by Django 4.0.4 on 2022-05-19 13:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cloudwareApp', '0003_alter_file_uploaded_file'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='shareddirectory',
            unique_together={('user', 'directory')},
        ),
    ]
