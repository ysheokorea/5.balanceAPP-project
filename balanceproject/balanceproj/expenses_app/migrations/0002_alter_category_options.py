# Generated by Django 3.2.8 on 2021-10-12 13:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expenses_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
    ]
