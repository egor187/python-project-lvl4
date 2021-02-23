# Generated by Django 3.1.6 on 2021-02-23 09:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_auto_20210223_0843'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='task_status',
            new_name='status',
        ),
        migrations.AlterField(
            model_name='relatedmodel',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.task'),
        ),
    ]
