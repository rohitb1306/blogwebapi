# Generated by Django 3.2.14 on 2022-07-25 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_myuser_new_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='user_contact',
            field=models.BigIntegerField(default=0, null=True),
        ),
    ]