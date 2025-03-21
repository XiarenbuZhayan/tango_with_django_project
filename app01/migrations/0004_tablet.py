# Generated by Django 5.1.7 on 2025-03-19 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app01", "0003_alter_phone_id_alter_phone_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="Tablet",
            fields=[
                (
                    "id",
                    models.AutoField(primary_key=True, serialize=False, unique=True),
                ),
                ("name", models.CharField(max_length=100)),
                ("size", models.CharField(max_length=50)),
                ("color", models.CharField(max_length=50)),
                ("storage", models.IntegerField()),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("stock", models.IntegerField(default=0)),
            ],
        ),
    ]
