# Generated by Django 2.1 on 2022-02-28 18:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0007_order_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='user',
        ),
    ]
