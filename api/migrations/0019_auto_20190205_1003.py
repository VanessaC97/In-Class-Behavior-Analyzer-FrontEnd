# Generated by Django 2.1.5 on 2019-02-05 15:03

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_auto_20190205_1000'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='title',
            field=models.CharField(default='Test Class', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='class',
            name='id',
            field=models.UUIDField(default=uuid.UUID('800099b8-4aee-4692-ade1-c82920393998'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='demographic',
            name='id',
            field=models.UUIDField(default=uuid.UUID('0f9c40ad-8f59-4675-8a07-eeffd4dc9c91'), primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='position',
            name='id',
            field=models.UUIDField(default=uuid.UUID('4ab3e89c-9d57-4ee8-87d1-101af1c25b5a'), editable=False, primary_key=True, serialize=False),
        ),
    ]
