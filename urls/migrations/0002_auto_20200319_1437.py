# Generated by Django 3.0.4 on 2020-03-19 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("urls", "0001_initial")]

    operations = [
        migrations.AlterField(
            model_name="url",
            name="original_url",
            field=models.URLField(max_length=400, verbose_name="URL"),
        )
    ]
