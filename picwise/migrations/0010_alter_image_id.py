# Generated by Django 3.2 on 2022-06-07 01:56

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('picwise', '0009_alter_image_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='id',
            field=models.UUIDField(default=uuid.UUID('cb4ca89e-2230-4fe3-a8d5-0df1d9333ace'), editable=False, primary_key=True, serialize=False),
        ),
    ]