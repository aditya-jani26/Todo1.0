# Generated by Django 5.0.2 on 2024-04-03 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0009_person_remove_task_user_id_todo_delete_customuser_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
