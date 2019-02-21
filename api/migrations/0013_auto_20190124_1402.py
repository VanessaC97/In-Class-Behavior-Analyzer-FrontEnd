# Generated by Django 2.1.5 on 2019-01-24 19:02

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_auto_20190124_1248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='id',
            field=models.UUIDField(default=uuid.UUID('aeb2bdfe-d32e-42cd-b8b6-3773a7eed4d2'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='student',
            name='reset_password_code',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]
