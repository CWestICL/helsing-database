# Generated by Django 4.1.3 on 2022-11-23 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("monsterdatabase", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="monster",
            name="description",
            field=models.TextField(blank=True),
        ),
    ]
