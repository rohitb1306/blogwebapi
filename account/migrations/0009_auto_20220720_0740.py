# Generated by Django 3.2.14 on 2022-07-20 07:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_alter_myuser_new_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='approved',
        ),
        migrations.RemoveField(
            model_name='myuser',
            name='new_user',
        ),
    ]
