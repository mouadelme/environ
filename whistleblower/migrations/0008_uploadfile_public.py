# Generated by Django 4.2.10 on 2024-04-20 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whistleblower', '0007_uploadfile_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadfile',
            name='public',
            field=models.BooleanField(default=False),
        ),
    ]