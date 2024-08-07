# Generated by Django 5.0.6 on 2024-06-30 19:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("books", "0002_author_cover_image"),
        ("users", "0007_alter_favorite_book"),
    ]

    operations = [
        migrations.AlterField(
            model_name="favorite",
            name="book",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="favorite",
                to="books.book",
            ),
        ),
    ]
