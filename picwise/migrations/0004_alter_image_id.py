# Generated by Django 3.2 on 2022-06-07 02:03

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('picwise', '0003_alter_image_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='id',
            field=models.UUIDField(default=uuid.UUID('1ced9670-4d11-414e-9553-bfe415f5371f'), editable=False, primary_key=True, serialize=False),
        ),
    ]
