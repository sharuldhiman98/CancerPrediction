# Generated by Django 3.0.5 on 2020-04-27 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_auto_20200427_1543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='profile_pic',
            field=models.ImageField(blank=True, upload_to='doctor'),
        ),
    ]
