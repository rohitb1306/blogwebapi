# Generated by Django 3.2.14 on 2022-07-28 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0028_alter_search_search_content"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blog",
            name="blog_image",
            field=models.ImageField(
                default="blog/image.jpg",
                null=True,
                upload_to="blog/images",
            ),
        ),
    ]
