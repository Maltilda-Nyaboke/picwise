# Generated by Django 3.2 on 2022-06-07 01:42

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('picwise', '0002_alter_image_uuid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='uuid',
        ),
        migrations.AddField(
            model_name='image',
            name='id',
            field=models.UUIDField(default=uuid.UUID('8e10ac04-3b8a-408a-9389-2b1d93403476'), editable=False, primary_key=True, serialize=False),
        ),
    ]
