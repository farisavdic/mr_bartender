# Generated by Django 4.2.1 on 2023-05-22 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cocktails', '0006_ingredient_garnish'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredient',
            name='available',
            field=models.BooleanField(default=False),
        ),
    ]
