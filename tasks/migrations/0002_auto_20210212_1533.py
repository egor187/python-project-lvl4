# Generated by Django 3.1.6 on 2021-02-12 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskstatus',
            name='name',
            field=models.CharField(choices=[('new', 'new task'), ('in_work', 'in working'), ('on_testing', 'on testing'), ('finished', 'fifnished')], max_length=70),
        ),
    ]