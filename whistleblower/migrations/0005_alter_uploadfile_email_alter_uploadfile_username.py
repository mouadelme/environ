# Generated by Django 4.2.10 on 2024-03-18 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whistleblower', '0004_uploadfile_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadfile',
            name='email',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='uploadfile',
            name='username',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
    ]
