# Generated by Django 2.1 on 2022-01-27 15:47

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0003_order_payment'),
    ]

    operations = [
        migrations.CreateModel(
            name='payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_amt', models.CharField(max_length=250)),
                ('bill_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('card_num', models.CharField(max_length=250)),
                ('month_year', models.CharField(max_length=10)),
                ('CVV_code', models.CharField(max_length=10)),
                ('paymentid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.Order')),
            ],
        ),
    ]
