# Generated by Django 4.0.4 on 2022-04-27 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloudwareApp', '0002_rename_sharedirectory_shareddirectory_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='uploadedFile',
            field=models.FileField(default=12, upload_to='Uploaded Files/'),
            preserve_default=False,
        ),
    ]
