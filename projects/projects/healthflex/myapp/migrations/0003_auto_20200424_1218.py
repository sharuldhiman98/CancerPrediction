# Generated by Django 3.0.5 on 2020-04-24 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_doctors'),
    ]

    operations = [
        migrations.CreateModel(
            name='doctor',
            fields=[
                ('name', models.CharField(max_length=30)),
                ('phoneno', models.BigIntegerField()),
                ('password', models.CharField(default='123456', max_length=20)),
                ('email', models.EmailField(max_length=254, primary_key=True, serialize=False)),
                ('profile_pic', models.ImageField(blank=True, upload_to='doctor')),
                ('Portfolio', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='hospital',
            fields=[
                ('name', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('phoneno', models.BigIntegerField()),
                ('address', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('profile_pic', models.ImageField(blank=True, upload_to='hospital')),
                ('Portfolio', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='medicine',
            fields=[
                ('Name', models.CharField(max_length=30)),
                ('Usage', models.CharField(max_length=30)),
                ('Manufacturer', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('Salts', models.CharField(max_length=300)),
            ],
        ),
        migrations.DeleteModel(
            name='doctors',
        ),
        migrations.RemoveField(
            model_name='person',
            name='id',
        ),
        migrations.AlterField(
            model_name='person',
            name='first_name',
            field=models.CharField(max_length=30, primary_key=True, serialize=False),
        ),
    ]
