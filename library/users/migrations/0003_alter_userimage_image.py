# Generated by Django 5.0.6 on 2024-06-30 12:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_alter_userimage_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userimage",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="user_images"),
        ),
    ]
