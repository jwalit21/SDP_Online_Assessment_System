# Generated by Django 3.1.5 on 2021-01-09 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210109_2214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='isStudent',
            field=models.BooleanField(default=False, verbose_name='student'),
        ),
    ]
