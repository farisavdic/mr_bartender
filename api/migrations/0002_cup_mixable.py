# Generated by Django 4.2.1 on 2023-05-16 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cup',
            name='mixable',
            field=models.BooleanField(default=False),
        ),
    ]
