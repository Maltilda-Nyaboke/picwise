# Generated by Django 3.2 on 2022-06-07 01:43

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('picwise', '0004_alter_image_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='id',
            field=models.UUIDField(default=uuid.UUID('19fbf086-53a1-4214-b556-a854de557ca8'), editable=False, primary_key=True, serialize=False),
        ),
    ]