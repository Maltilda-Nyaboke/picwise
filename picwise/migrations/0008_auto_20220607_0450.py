# Generated by Django 3.2 on 2022-06-07 01:50

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('picwise', '0007_auto_20220607_0447'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='uuid',
        ),
        migrations.AddField(
            model_name='image',
            name='id',
            field=models.UUIDField(default=uuid.UUID('b42b251d-722c-4559-aeb0-e30110f02c91'), editable=False, primary_key=True, serialize=False),
        ),
    ]