# Generated by Django 3.2.14 on 2022-07-21 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0014_auto_20220721_1127"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blog",
            name="blog_title",
            field=models.CharField(max_length=150, unique=True),
        ),
    ]
