# Generated by Django 5.0.6 on 2024-06-23 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_post_author_post_status_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="slug",
            field=models.SlugField(max_length=250, unique_for_date="publish"),
        ),
    ]
