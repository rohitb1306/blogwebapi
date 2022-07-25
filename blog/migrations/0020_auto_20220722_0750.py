# Generated by Django 3.2.14 on 2022-07-22 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0019_alter_blog_blog_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='blog_rating',
        ),
        migrations.AddField(
            model_name='blog',
            name='blog_discription',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='blog',
            name='blog_keywords',
            field=models.CharField(max_length=150, null=True),
        ),
    ]