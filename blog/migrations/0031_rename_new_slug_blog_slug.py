# Generated by Django 4.0.6 on 2022-08-03 06:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0030_alter_blog_blog_image"),
    ]

    operations = [
        migrations.RenameField(
            model_name="blog",
            old_name="new_slug",
            new_name="slug",
        ),
    ]
