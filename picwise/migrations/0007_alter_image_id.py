# Generated by Django 3.2 on 2022-06-07 02:04

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('picwise', '0006_alter_image_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='id',
            field=models.UUIDField(default=uuid.UUID('610011db-53c9-4468-8bfb-2c814f41b616'), editable=False, primary_key=True, serialize=False),
        ),
    ]
