# Generated by Django 5.1.7 on 2025-03-18 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app01", "0002_phone_stock"),
    ]

    operations = [
        migrations.AlterField(
            model_name="phone",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name="phone",
            name="name",
            field=models.CharField(max_length=100),
        ),
    ]
