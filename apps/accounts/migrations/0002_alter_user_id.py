# Generated by Django 4.2.6 on 2024-01-06 23:14

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.UUIDField(default=uuid.UUID('60bab47c-1541-4777-8e5e-18bc4e2b23dc'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]