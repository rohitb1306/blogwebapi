# Generated by Django 3.2.14 on 2022-07-26 04:14

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_myuser_user_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='new_slug',
            field=autoslug.fields.AutoSlugField(default=None, editable=False, null=True, populate_from='user_name'),
        ),
    ]
