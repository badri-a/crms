# Generated by Django 2.1 on 2022-04-19 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0008_remove_order_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='cell_no',
            field=models.CharField(max_length=10),
        ),
    ]
