# Generated by Django 4.2.10 on 2024-03-17 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whistleblower', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadfile',
            name='email',
            field=models.CharField(default='anon', max_length=50),
        ),
    ]
