# Generated by Django 3.2.14 on 2022-07-15 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="myUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "password",
                    models.CharField(max_length=128, verbose_name="password"),
                ),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("f_name", models.CharField(default="", max_length=30)),
                ("l_name", models.CharField(default="", max_length=30)),
                ("u_name", models.CharField(max_length=30, unique=True)),
                ("is_auther", models.BooleanField(default=False)),
                ("is_staff", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=False)),
                ("image", models.ImageField(default="", upload_to="")),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
