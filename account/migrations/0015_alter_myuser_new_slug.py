# Generated by Django 3.2.14 on 2022-07-26 09:45

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_alter_myuser_new_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='new_slug',
            field=autoslug.fields.AutoSlugField(default=None, editable=False, null=True, populate_from='user_name'),
        ),
    ]
