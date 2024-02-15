# Generated by Django 5.0.1 on 2024-02-15 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=500, unique=True)),
                ('password', models.CharField(max_length=500)),
            ],
        ),
    ]