# Generated by Django 3.2.14 on 2022-07-18 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0004_auto_20220718_1147"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="comment",
            name="rating",
        ),
        migrations.AddField(
            model_name="blog",
            name="rating",
            field=models.IntegerField(default=0),
        ),
    ]
